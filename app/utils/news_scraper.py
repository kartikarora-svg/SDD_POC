"""News scraper using RSS feeds"""
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
from app.config import settings


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parse date string from RSS feed.
    
    Args:
        date_str: Date string from feed
        
    Returns:
        Datetime object or None
    """
    if not date_str:
        return None
    
    try:
        # feedparser provides struct_time
        import time
        parsed = feedparser._parse_date(date_str)
        if parsed:
            return datetime(*parsed[:6])
    except:
        pass
    
    return None


def scrape_rss_feed(feed_url: str, source_name: str) -> List[Dict]:
    """
    Scrape articles from an RSS feed.
    
    Args:
        feed_url: URL of the RSS feed
        source_name: Name of the source (e.g., "CNBC")
        
    Returns:
        List of article dictionaries
    """
    articles = []
    
    try:
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            # Extract article data
            article = {
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'source': source_name,
                'description': entry.get('summary', '') or entry.get('description', ''),
                'published_at': parse_date(entry.get('published', '')),
            }
            
            # Only add if we have minimum required fields
            if article['title'] and article['url']:
                articles.append(article)
        
        return articles
        
    except Exception as e:
        print(f"Error scraping {source_name}: {e}")
        return []


def scrape_all_sources() -> List[Dict]:
    """
    Scrape all configured news sources.
    
    Returns:
        List of all articles from all sources
    """
    all_articles = []
    
    for source_name, feed_url in settings.NEWS_SOURCES.items():
        articles = scrape_rss_feed(feed_url, source_name)
        all_articles.extend(articles)
        print(f"Scraped {len(articles)} articles from {source_name}")
    
    return all_articles


def get_article_content(url: str) -> Optional[str]:
    """
    Fetch full article content from URL.
    For MVP, we'll use the description from RSS.
    This can be enhanced later with web scraping.
    
    Args:
        url: Article URL
        
    Returns:
        Article content or None
    """
    # For now, return None - we'll use description from RSS
    # Future enhancement: Use newspaper3k or BeautifulSoup to scrape full content
    return None

