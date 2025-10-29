"""Export model for tracking document exports"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
import enum
from app.database import Base


class ExportFormat(str, enum.Enum):
    """Export format types"""
    PDF = "pdf"
    DOCX = "docx"
    EMAIL = "email"


class Export(Base):
    """Model for tracking document exports"""
    
    __tablename__ = "exports"
    
    # Primary key
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    
    # References
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    document_id = Column(
        String(36),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Export details
    format = Column(
        SQLEnum(ExportFormat),
        nullable=False
    )
    file_path = Column(
        String(512),
        nullable=True  # Null for email exports
    )
    recipient_email = Column(
        String(255),
        nullable=True  # Only for email exports
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        return f"<Export(id={self.id}, format={self.format}, document_id={self.document_id})>"

