"""News feed API endpoints"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.user import User
from app.models.news import NewsArticle
from app.schemas.news import (
    NewsArticleResponse,
    NewsSummarizeRequest,
    NewsSummaryResponse
)
from app.utils.auth import get_current_user
from app.utils.news_scraper import scrape_all_sources
from app.utils.news_summarizer import summarize_article

router = APIRouter()


async def scrape_news_background(db: Session):
    """
    Background task to scrape news from all sources.
    
    Args:
        db: Database session
    """
    try:
        # Scrape all sources
        articles = scrape_all_sources()
        
        # Save to database (skip duplicates)
        new_count = 0
        for article_data in articles:
            try:
                # Check if article already exists
                existing = db.query(NewsArticle).filter(
                    NewsArticle.url == article_data['url']
                ).first()
                
                if not existing:
                    article = NewsArticle(
                        title=article_data['title'],
                        url=article_data['url'],
                        source=article_data['source'],
                        description=article_data['description'],
                        published_at=article_data['published_at']
                    )
                    db.add(article)
                    db.flush()  # Catch constraint errors early
                    new_count += 1
            except Exception:
                # Skip duplicates silently
                db.rollback()
                continue
        
        db.commit()
        print(f"Successfully saved {new_count} new articles")
        
    except Exception as e:
        print(f"Error in background scraping: {e}")
        db.rollback()


@router.get("/", response_model=List[NewsArticleResponse])
async def get_news_feed(
    limit: int = 50,
    source: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get latest financial news articles.
    
    - **limit**: Maximum number of articles to return (default: 50)
    - **source**: Filter by source (optional)
    
    Returns list of news articles ordered by published date.
    """
    query = db.query(NewsArticle)
    
    if source:
        query = query.filter(NewsArticle.source == source)
    
    articles = query.order_by(desc(NewsArticle.published_at)).limit(limit).all()
    
    return articles


@router.get("/sources")
async def get_news_sources(
    current_user: User = Depends(get_current_user)
):
    """
    Get list of available news sources.
    """
    from app.config import settings
    return {
        "sources": list(settings.NEWS_SOURCES.keys())
    }


@router.get("/{article_id}", response_model=NewsArticleResponse)
async def get_article(
    article_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific news article by ID.
    """
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )
    
    return article


@router.post("/{article_id}/summarize", response_model=NewsSummaryResponse)
async def summarize_news_article(
    article_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI summary for a news article.
    
    - **article_id**: ID of the article to summarize
    
    Returns AI-generated summary.
    """
    # Get article
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )
    
    # Check if summary already exists
    if article.ai_summary and article.summary_generated:
        return {
            "article_id": article_id,
            "summary": article.ai_summary,
            "generated_at": article.scraped_at
        }
    
    # Generate summary
    summary = await summarize_article(
        title=article.title,
        description=article.description or "",
        url=article.url
    )
    
    if not summary:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate summary"
        )
    
    # Save summary
    article.ai_summary = summary
    article.summary_generated = True
    db.commit()
    
    return {
        "article_id": article_id,
        "summary": summary,
        "generated_at": datetime.utcnow()
    }


@router.post("/scrape", status_code=status.HTTP_202_ACCEPTED)
async def trigger_news_scrape(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger news scraping (admin function).
    Scraping runs in background.
    """
    background_tasks.add_task(scrape_news_background, db)
    
    return {
        "message": "News scraping started in background",
        "status": "processing"
    }


@router.get("/stats/overview")
async def get_news_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics about the news feed.
    """
    total_articles = db.query(NewsArticle).count()
    
    # Count by source
    from sqlalchemy import func
    by_source = db.query(
        NewsArticle.source,
        func.count(NewsArticle.id).label('count')
    ).group_by(NewsArticle.source).all()
    
    # Count summarized articles
    summarized = db.query(NewsArticle).filter(
        NewsArticle.summary_generated == True
    ).count()
    
    return {
        "total_articles": total_articles,
        "summarized_articles": summarized,
        "by_source": {source: count for source, count in by_source}
    }

