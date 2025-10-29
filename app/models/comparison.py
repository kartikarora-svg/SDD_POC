"""Stock comparison model"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from app.database import Base


class StockComparison(Base):
    """Model for storing stock comparison results"""
    
    __tablename__ = "stock_comparisons"
    
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
    
    # Comparison details
    ticker1 = Column(
        String(10),
        nullable=False
    )
    ticker2 = Column(
        String(10),
        nullable=False
    )
    
    # Comparison data (JSON stored as text)
    comparison_data = Column(
        Text,
        nullable=False
    )
    
    # AI-generated summary
    ai_summary = Column(
        Text,
        nullable=False
    )
    
    # Timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        return f"<StockComparison(id={self.id}, tickers={self.ticker1} vs {self.ticker2})>"

