"""Stock query models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float
from app.database import Base


class StockQuery(Base):
    """Model for storing stock query history"""
    
    __tablename__ = "stock_queries"
    
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
    
    # Stock details
    ticker = Column(
        String(10),
        nullable=False,
        index=True
    )
    question = Column(
        Text,
        nullable=False
    )
    answer = Column(
        Text,
        nullable=False
    )
    
    # Stock data snapshot (at time of query)
    current_price = Column(
        Float,
        nullable=True
    )
    market_cap = Column(
        Float,
        nullable=True
    )
    
    # Timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        return f"<StockQuery(id={self.id}, ticker={self.ticker}, question={self.question[:50]})>"

