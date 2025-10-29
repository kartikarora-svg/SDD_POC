"""News article model for financial news feed"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Boolean
from app.database import Base


class NewsArticle(Base):
    """Model for storing scraped financial news articles"""
    
    __tablename__ = "news_articles"
    
    # Primary key
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    
    # Article metadata
    title = Column(
        String(500),
        nullable=False
    )
    url = Column(
        String(1000),
        nullable=False,
        unique=True,  # Prevent duplicates
        index=True
    )
    source = Column(
        String(100),
        nullable=False,
        index=True
    )
    
    # Content
    description = Column(
        Text,
        nullable=True
    )
    content = Column(
        Text,
        nullable=True
    )
    
    # AI-generated summary
    ai_summary = Column(
        Text,
        nullable=True
    )
    summary_generated = Column(
        Boolean,
        nullable=False,
        default=False
    )
    
    # Timestamps
    published_at = Column(
        DateTime,
        nullable=True
    )
    scraped_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        return f"<NewsArticle(id={self.id}, title={self.title[:50]}, source={self.source})>"

