"""News-related Pydantic schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class NewsArticleResponse(BaseModel):
    """Schema for news article response"""
    id: str
    title: str
    url: str
    source: str
    description: Optional[str] = None
    ai_summary: Optional[str] = None
    summary_generated: bool
    published_at: Optional[datetime] = None
    scraped_at: datetime
    
    class Config:
        from_attributes = True


class NewsSummarizeRequest(BaseModel):
    """Schema for requesting AI summary"""
    article_id: str


class NewsSummaryResponse(BaseModel):
    """Schema for AI summary response"""
    article_id: str
    summary: str
    generated_at: datetime

