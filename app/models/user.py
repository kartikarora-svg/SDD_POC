"""User model for authentication"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    # Primary key (UUID stored as string for SQLite compatibility)
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False
    )
    
    # Authentication fields
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = Column(
        String(255),
        nullable=False
    )
    
    # Account status
    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    last_login = Column(
        DateTime,
        nullable=True
    )
    
    # Relationships (will be used by other models)
    # These are defined here but actual relationship() calls are in respective models
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

