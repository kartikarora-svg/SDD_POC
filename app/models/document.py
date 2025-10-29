"""Document model for uploaded files"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class DocumentStatus(str, enum.Enum):
    """Document processing status"""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    """Model for uploaded financial documents"""
    
    __tablename__ = "documents"
    
    # Primary key
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    
    # Owner
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # File information
    filename = Column(
        String(255),
        nullable=False
    )
    original_filename = Column(
        String(255),
        nullable=False
    )
    file_path = Column(
        String(512),
        nullable=False
    )
    file_size = Column(
        Integer,
        nullable=False
    )
    mime_type = Column(
        String(100),
        nullable=False
    )
    
    # Processing
    status = Column(
        SQLEnum(DocumentStatus),
        nullable=False,
        default=DocumentStatus.UPLOADING
    )
    
    # Extracted content
    extracted_text = Column(
        Text,
        nullable=True
    )
    page_count = Column(
        Integer,
        nullable=True
    )
    
    # Error tracking
    error_message = Column(
        Text,
        nullable=True
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    processed_at = Column(
        DateTime,
        nullable=True
    )
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename}, status={self.status})>"

