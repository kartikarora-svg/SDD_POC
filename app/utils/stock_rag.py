"""Stock RAG agent for natural language queries using Groq"""
from typing import Tuple, Optional
from groq import Groq
from app.config import settings
from app.utils.stock_data import get_stock_data, format_large_number


async def query_stock(ticker: str, question: str) -> Tuple[str, Optional[dict]]:
    """
    Query stock using RAG with Yahoo Finance data and Groq LLM.
    
    Args:
        ticker: Stock ticker symbol
        question: User's question about the stock
        
    Returns:
        Tuple of (answer, stock_data)
    """
    # Check if API key is set
    if not settings.GROQ_API_KEY:
        return (
            "Groq API key not configured. Please set GROQ_API_KEY in your environment variables.",
            None
        )
    
    try:
        # Fetch stock data
        stock_data = get_stock_data(ticker)
        
        if not stock_data:
            return (f"Could not fetch data for ticker '{ticker}'. Please verify the ticker symbol.", None)
        
        # Build context from stock data
        context = build_stock_context(stock_data)
        
        # Initialize Groq client
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Build prompt
        prompt = f"""You are a financial analyst assistant. Answer the user's question about this stock based on the provided data.

Stock: {stock_data['name']} ({ticker.upper()})

Current Data:
{context}

User Question: {question}

Instructions:
- Answer based ONLY on the provided stock data
- Be specific and cite relevant numbers
- If the data doesn't contain the answer, say so
- Keep your answer concise and focused
- Use professional financial language

Answer:"""
        
        # Call Groq API
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable financial analyst. Provide accurate, data-driven answers about stocks."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=512
        )
        
        answer = response.choices[0].message.content.strip()
        
        return answer, stock_data
        
    except Exception as e:
        error_msg = f"Error analyzing stock: {str(e)}"
        return error_msg, None


def build_stock_context(stock_data: dict) -> str:
    """Build formatted context string from stock data"""
    context_parts = []
    
    # Price and valuation
    if stock_data.get('current_price'):
        context_parts.append(f"Current Price: ${stock_data['current_price']:.2f}")
    
    if stock_data.get('market_cap_formatted'):
        context_parts.append(f"Market Cap: {stock_data['market_cap_formatted']}")
    
    if stock_data.get('pe_ratio'):
        context_parts.append(f"P/E Ratio: {stock_data['pe_ratio']:.2f}")
    
    # Price range
    if stock_data.get('week_52_high') and stock_data.get('week_52_low'):
        context_parts.append(
            f"52-Week Range: ${stock_data['week_52_low']:.2f} - ${stock_data['week_52_high']:.2f}"
        )
    
    # Trading volume
    if stock_data.get('volume') and stock_data.get('avg_volume'):
        context_parts.append(
            f"Volume: {stock_data['volume']:,} (Avg: {stock_data['avg_volume']:,})"
        )
    
    # Dividend
    if stock_data.get('dividend_yield'):
        context_parts.append(f"Dividend Yield: {stock_data['dividend_yield']*100:.2f}%")
    
    # Company info
    if stock_data.get('sector'):
        context_parts.append(f"Sector: {stock_data['sector']}")
    
    if stock_data.get('industry'):
        context_parts.append(f"Industry: {stock_data['industry']}")
    
    # Financial metrics
    if stock_data.get('revenue'):
        revenue_formatted = format_large_number(stock_data['revenue'])
        context_parts.append(f"Revenue: {revenue_formatted}")
    
    if stock_data.get('profit_margins'):
        context_parts.append(f"Profit Margin: {stock_data['profit_margins']*100:.2f}%")
    
    if stock_data.get('earnings_growth'):
        context_parts.append(f"Earnings Growth: {stock_data['earnings_growth']*100:.2f}%")
    
    if stock_data.get('debt_to_equity'):
        context_parts.append(f"Debt-to-Equity: {stock_data['debt_to_equity']:.2f}")
    
    if stock_data.get('beta'):
        context_parts.append(f"Beta: {stock_data['beta']:.2f}")
    
    # Description
    if stock_data.get('description'):
        desc = stock_data['description'][:500]  # Limit length
        context_parts.append(f"\nCompany Description: {desc}...")
    
    return "\n".join(context_parts)

