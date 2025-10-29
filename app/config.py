"""
Application configuration management
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Finalytics MVP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    # SQLite (default): sqlite:///./finalytics.db
    # PostgreSQL: postgresql://user:password@localhost:5432/finalytics
    # MySQL: mysql+pymysql://user:password@localhost:3306/finalytics
    DATABASE_URL: str = "sqlite:///./finalytics.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "your-secret-key-here-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Groq API
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    
    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_data"
    
    # File Storage
    STORAGE_DIR: str = "./storage"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB in bytes
    
    # Email (Gmail SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    # News Sources (RSS Feeds)
    NEWS_SOURCES: dict = {
        "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "BBC": "http://feeds.bbci.co.uk/news/business/rss.xml",
        "TechCrunch": "https://techcrunch.com/feed/"
    }
    NEWS_SCRAPE_INTERVAL_MINUTES: int = 5
    NEWS_CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # OCR Settings
    TESSERACT_CMD: Optional[str] = None  # Path to tesseract executable if not in PATH
    POPPLER_PATH: Optional[str] = None  # Path to poppler bin directory
    
    # Chunking Strategy
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    
    # Performance
    MAX_CONCURRENT_USERS: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

