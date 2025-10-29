"""Document-related Pydantic schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DocumentUpload(BaseModel):
    """Schema for document upload response"""
    id: str
    filename: str
    file_size: int
    status: str
    message: str


class DocumentResponse(BaseModel):
    """Schema for document details"""
    id: str
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    status: str
    page_count: Optional[int] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class DocumentQuery(BaseModel):
    """Schema for document Q&A query"""
    question: str = Field(..., min_length=3, description="Question about the document")


class DocumentAnswer(BaseModel):
    """Schema for document Q&A answer"""
    question: str
    answer: str
    context: Optional[str] = None
    

class QueryHistoryResponse(BaseModel):
    """Schema for query history item"""
    id: str
    question: str
    answer: str
    created_at: datetime
    
    class Config:
        from_attributes = True

