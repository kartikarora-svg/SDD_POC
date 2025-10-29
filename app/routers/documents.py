"""Document management API endpoints"""
import asyncio
import threading
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.models.query_history import QueryHistory
from app.schemas.document import (
    DocumentUpload,
    DocumentResponse,
    DocumentQuery,
    DocumentAnswer,
    QueryHistoryResponse
)
from app.utils.auth import get_current_user
from app.utils.file_handler import validate_file, save_upload_file
from app.utils.text_extractor import extract_text
from app.utils.llm_client import query_document

router = APIRouter()


def process_document_in_thread(document_id: str, file_path: str, mime_type: str):
    """
    Process document in a separate thread to avoid blocking other features.
    This runs completely independently from the main application.
    
    Args:
        document_id: Document ID
        file_path: Path to uploaded file
        mime_type: MIME type of file
    """
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        print(f"[Thread-{threading.current_thread().name}] Starting text extraction for document {document_id}")
        
        # Extract text with parallel processing
        extracted_text, page_count = extract_text(file_path, mime_type)
        print(f"[Thread-{threading.current_thread().name}] Text extraction completed. Length: {len(extracted_text)} characters")
        
        # Update document in database
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            document.extracted_text = extracted_text
            document.page_count = page_count
            document.status = DocumentStatus.COMPLETED
            document.processed_at = datetime.utcnow()
            db.commit()
            print(f"[Thread-{threading.current_thread().name}] Document {document_id} processed successfully")
            
    except Exception as e:
        print(f"[Thread-{threading.current_thread().name}] Error processing document {document_id}: {str(e)}")
        # Mark document as failed
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                document.status = DocumentStatus.FAILED
                document.error_message = str(e)
                db.commit()
        except Exception as db_error:
            print(f"[Thread-{threading.current_thread().name}] Error updating document status: {str(db_error)}")
    finally:
        db.close()
        print(f"[Thread-{threading.current_thread().name}] Processing thread completed for document {document_id}")


@router.post("/upload", response_model=DocumentUpload, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document (PDF or image) for analysis.
    
    - **file**: PDF or image file (max 50MB)
    
    The document will be processed asynchronously.
    Check status with GET /documents/{document_id}
    """
    # Validate file
    validate_file(file)
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > 52428800:  # 50MB
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 50MB limit"
        )
    
    # Save file
    file_path, unique_filename, actual_size = await save_upload_file(file, str(current_user.id))
    
    # Create document record
    document = Document(
        user_id=str(current_user.id),
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=actual_size,
        mime_type=file.content_type,
        status=DocumentStatus.PROCESSING
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Process document in a completely separate thread (non-blocking)
    # This ensures other API features remain available during processing
    processing_thread = threading.Thread(
        target=process_document_in_thread,
        args=(str(document.id), file_path, file.content_type),
        daemon=True,  # Daemon thread won't block app shutdown
        name=f"DocProcessor-{document.id[:8]}"
    )
    processing_thread.start()
    print(f"Started independent processing thread: {processing_thread.name}")
    
    return {
        "id": str(document.id),
        "filename": file.filename,
        "file_size": actual_size,
        "status": document.status.value,
        "message": "Document uploaded successfully. Processing independently in background."
    }


async def _list_documents_impl(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all documents for the current user.
    """
    documents = db.query(Document)\
        .filter(Document.user_id == str(current_user.id))\
        .order_by(Document.created_at.desc())\
        .all()
    
    return documents


@router.get("/", response_model=List[DocumentResponse])
async def list_documents_slash(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents for the current user (with trailing slash)."""
    return await _list_documents_impl(current_user, db)


@router.get("", response_model=List[DocumentResponse])
async def list_documents_no_slash(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents for the current user (without trailing slash)."""
    return await _list_documents_impl(current_user, db)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document details and processing status.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    return document


@router.post("/{document_id}/query", response_model=DocumentAnswer)
async def query_document_endpoint(
    document_id: str,
    query: DocumentQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ask a question about a document.
    
    - **document_id**: ID of the processed document
    - **question**: Your question about the document
    
    Returns an AI-generated answer based on the document content.
    """
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    if document.status != DocumentStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Document is not ready. Status: {document.status.value}"
        )
    
    if not document.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Document has no extracted text"
        )
    
    # Query document using LLM
    answer, context = await query_document(
        question=query.question,
        document_text=document.extracted_text,
        document_name=document.original_filename
    )
    
    # Save query history
    query_history = QueryHistory(
        user_id=str(current_user.id),
        document_id=document_id,
        question=query.question,
        answer=answer,
        context_chunks=context
    )
    
    db.add(query_history)
    db.commit()
    
    return {
        "question": query.question,
        "answer": answer,
        "context": context
    }


@router.get("/{document_id}/history", response_model=List[QueryHistoryResponse])
async def get_query_history(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get Q&A history for a document.
    """
    # Verify document ownership
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    # Get history
    history = db.query(QueryHistory)\
        .filter(QueryHistory.document_id == document_id)\
        .order_by(QueryHistory.created_at.desc())\
        .all()
    
    return history


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document and its associated data.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    # Delete file
    try:
        import os
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    # Delete database record (cascades to query_history)
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

