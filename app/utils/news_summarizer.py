"""AI-powered news summarization using Groq"""
from typing import Optional
from groq import Groq
from app.config import settings


async def summarize_article(title: str, description: str, url: str) -> Optional[str]:
    """
    Generate AI summary of a news article.
    
    Args:
        title: Article title
        description: Article description/excerpt
        url: Article URL
        
    Returns:
        AI-generated summary or None if error
    """
    # Check if API key is set
    if not settings.GROQ_API_KEY:
        return "Groq API key not configured. Please set GROQ_API_KEY to enable AI summaries."
    
    try:
        # Initialize Groq client
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Build prompt
        prompt = f"""You are a financial news analyst. Summarize this news article in 2-3 concise sentences.
Focus on the key facts and their potential market impact.

Title: {title}

Content: {description}

Provide a clear, factual summary that highlights:
1. The main news/event
2. Key figures or developments
3. Potential market implications (if relevant)

Summary:"""
        
        # Call Groq API
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial news analyst. Provide concise, factual summaries."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=256
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"Error generating summary: {str(e)}"

