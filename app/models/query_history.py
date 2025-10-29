"""Query history model for document Q&A"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.database import Base


class QueryHistory(Base):
    """Model for storing document Q&A history"""
    
    __tablename__ = "query_history"
    
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
    
    # Q&A content
    question = Column(
        Text,
        nullable=False
    )
    answer = Column(
        Text,
        nullable=False
    )
    
    # Context used for answer
    context_chunks = Column(
        Text,
        nullable=True
    )
    
    # Timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        return f"<QueryHistory(id={self.id}, document_id={self.document_id})>"

