"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Database-specific configuration
connect_args = {}
engine_args = {"echo": settings.DEBUG}

if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite-specific: allow same connection across threads
    connect_args = {"check_same_thread": False}
elif settings.DATABASE_URL.startswith("postgresql"):
    # PostgreSQL-specific: connection pool settings
    engine_args.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,  # Verify connections before using
        "pool_recycle": 3600  # Recycle connections every hour
    })

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    **engine_args
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Dependency function that yields database sessions.
    Ensures sessions are properly closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

