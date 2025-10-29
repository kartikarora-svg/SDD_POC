"""Export API endpoints"""
import os
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.models.query_history import QueryHistory
from app.models.export import Export, ExportFormat
from app.schemas.export import ExportRequest, EmailExportRequest, ExportResponse
from app.utils.auth import get_current_user
from app.utils.pdf_exporter import create_pdf_export
from app.utils.docx_exporter import create_docx_export
from app.utils.email_sender import send_email, create_analysis_email_body
from app.config import settings

router = APIRouter()


@router.post("/pdf", response_model=ExportResponse)
async def export_to_pdf(
    export_request: ExportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export document Q&A to PDF.
    
    - **document_id**: ID of the document to export
    
    Returns download URL for the generated PDF.
    """
    document_id = export_request.document_id
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.status != DocumentStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Document is not ready. Status: {document.status.value}"
        )
    
    # Get Q&A history
    qa_history = db.query(QueryHistory).filter(
        QueryHistory.document_id == document_id
    ).order_by(QueryHistory.created_at).all()
    
    if not qa_history:
        raise HTTPException(
            status_code=400,
            detail="No Q&A history found for this document"
        )
    
    # Prepare Q&A data
    qa_data = [
        {
            'question': qa.question,
            'answer': qa.answer,
            'created_at': qa.created_at.isoformat()
        }
        for qa in qa_history
    ]
    
    # Create exports directory
    exports_dir = Path(settings.STORAGE_DIR) / str(current_user.id) / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{document.original_filename.rsplit('.', 1)[0]}_analysis_{timestamp}.pdf"
    output_path = exports_dir / filename
    
    # Create PDF
    create_pdf_export(
        document_name=document.original_filename,
        qa_history=qa_data,
        output_path=str(output_path)
    )
    
    # Save export record
    export_record = Export(
        user_id=str(current_user.id),
        document_id=document_id,
        format=ExportFormat.PDF,
        file_path=str(output_path)
    )
    db.add(export_record)
    db.commit()
    db.refresh(export_record)
    
    return {
        "export_id": str(export_record.id),
        "format": "pdf",
        "file_path": str(output_path),
        "download_url": f"/api/exports/download/{export_record.id}",
        "message": "PDF export created successfully",
        "created_at": export_record.created_at
    }


@router.post("/docx", response_model=ExportResponse)
async def export_to_docx(
    export_request: ExportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export document Q&A to Word document.
    
    - **document_id**: ID of the document to export
    
    Returns download URL for the generated DOCX file.
    """
    document_id = export_request.document_id
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.status != DocumentStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Document is not ready. Status: {document.status.value}"
        )
    
    # Get Q&A history
    qa_history = db.query(QueryHistory).filter(
        QueryHistory.document_id == document_id
    ).order_by(QueryHistory.created_at).all()
    
    if not qa_history:
        raise HTTPException(
            status_code=400,
            detail="No Q&A history found for this document"
        )
    
    # Prepare Q&A data
    qa_data = [
        {
            'question': qa.question,
            'answer': qa.answer,
            'created_at': qa.created_at.isoformat()
        }
        for qa in qa_history
    ]
    
    # Create exports directory
    exports_dir = Path(settings.STORAGE_DIR) / str(current_user.id) / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{document.original_filename.rsplit('.', 1)[0]}_analysis_{timestamp}.docx"
    output_path = exports_dir / filename
    
    # Create DOCX
    create_docx_export(
        document_name=document.original_filename,
        qa_history=qa_data,
        output_path=str(output_path)
    )
    
    # Save export record
    export_record = Export(
        user_id=str(current_user.id),
        document_id=document_id,
        format=ExportFormat.DOCX,
        file_path=str(output_path)
    )
    db.add(export_record)
    db.commit()
    db.refresh(export_record)
    
    return {
        "export_id": str(export_record.id),
        "format": "docx",
        "file_path": str(output_path),
        "download_url": f"/api/exports/download/{export_record.id}",
        "message": "Word document export created successfully",
        "created_at": export_record.created_at
    }


@router.post("/email", status_code=status.HTTP_202_ACCEPTED)
async def email_export(
    email_request: EmailExportRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Email document Q&A analysis.
    
    - **document_id**: ID of the document to export
    - **recipient_email**: Email address to send to
    - **format**: Export format ('pdf' or 'docx')
    
    Sends email in background.
    """
    document_id = email_request.document_id
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == str(current_user.id)
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.status != DocumentStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Document is not ready. Status: {document.status.value}"
        )
    
    # Get Q&A history
    qa_history = db.query(QueryHistory).filter(
        QueryHistory.document_id == document_id
    ).order_by(QueryHistory.created_at).all()
    
    if not qa_history:
        raise HTTPException(
            status_code=400,
            detail="No Q&A history found for this document"
        )
    
    # Prepare Q&A data
    qa_data = [
        {
            'question': qa.question,
            'answer': qa.answer,
            'created_at': qa.created_at.isoformat()
        }
        for qa in qa_history
    ]
    
    # Create exports directory
    exports_dir = Path(settings.STORAGE_DIR) / str(current_user.id) / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_ext = 'pdf' if email_request.format == 'pdf' else 'docx'
    filename = f"{document.original_filename.rsplit('.', 1)[0]}_analysis_{timestamp}.{file_ext}"
    output_path = exports_dir / filename
    
    # Create export file
    if email_request.format == 'pdf':
        create_pdf_export(document.original_filename, qa_data, str(output_path))
    else:
        create_docx_export(document.original_filename, qa_data, str(output_path))
    
    # Save export record
    export_record = Export(
        user_id=str(current_user.id),
        document_id=document_id,
        format=ExportFormat.EMAIL,
        file_path=str(output_path),
        recipient_email=email_request.recipient_email
    )
    db.add(export_record)
    db.commit()
    
    # Send email in background
    background_tasks.add_task(
        send_export_email,
        email_request.recipient_email,
        document.original_filename,
        len(qa_history),
        str(output_path)
    )
    
    return {
        "message": "Email is being sent in background",
        "recipient": email_request.recipient_email,
        "format": email_request.format
    }


async def send_export_email(
    recipient: str,
    document_name: str,
    qa_count: int,
    attachment_path: str
):
    """Background task to send export email"""
    try:
        subject = f"Your Document Analysis Report - {document_name}"
        body = create_analysis_email_body(document_name, qa_count)
        
        send_email(
            to_email=recipient,
            subject=subject,
            body=body,
            attachment_path=attachment_path
        )
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")


@router.get("/download/{export_id}")
async def download_export(
    export_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download an exported file.
    
    - **export_id**: ID of the export to download
    """
    # Get export record
    export_record = db.query(Export).filter(
        Export.id == export_id,
        Export.user_id == str(current_user.id)
    ).first()
    
    if not export_record:
        raise HTTPException(
            status_code=404, 
            detail="Export not found or you don't have permission to access it"
        )
    
    if not export_record.file_path or not os.path.exists(export_record.file_path):
        raise HTTPException(status_code=404, detail="Export file not found")
    
    # Determine media type
    if export_record.format == ExportFormat.PDF:
        media_type = "application/pdf"
    elif export_record.format == ExportFormat.DOCX:
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        media_type = "application/octet-stream"
    
    filename = Path(export_record.file_path).name
    
    return FileResponse(
        path=export_record.file_path,
        media_type=media_type,
        filename=filename
    )

