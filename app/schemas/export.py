"""Export-related Pydantic schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ExportRequest(BaseModel):
    """Schema for export request"""
    document_id: str
    format: str  # 'pdf' or 'docx'


class EmailExportRequest(BaseModel):
    """Schema for email export request"""
    document_id: str
    recipient_email: EmailStr
    format: str = 'pdf'  # 'pdf' or 'docx'


class ExportResponse(BaseModel):
    """Schema for export response"""
    export_id: str
    format: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

