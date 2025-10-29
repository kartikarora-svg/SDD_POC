"""Stock comparison utility with AI analysis"""
import json
from typing import Dict, Tuple, Optional
from groq import Groq
from app.config import settings
from app.utils.stock_data import get_stock_data


async def compare_stocks(ticker1: str, ticker2: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Compare two stocks and generate AI analysis.
    
    Args:
        ticker1: First stock ticker
        ticker2: Second stock ticker
        
    Returns:
        Tuple of (comparison_data, ai_summary)
    """
    # Check if API key is set
    if not settings.GROQ_API_KEY:
        return (
            None,
            "Groq API key not configured. Please set GROQ_API_KEY in your environment variables."
        )
    
    try:
        # Fetch data for both stocks
        stock1_data = get_stock_data(ticker1)
        stock2_data = get_stock_data(ticker2)
        
        if not stock1_data or not stock2_data:
            return (None, f"Could not fetch data for one or both tickers")
        
        # Build comparison data
        comparison = {
            'stock1': {
                'ticker': stock1_data['ticker'],
                'name': stock1_data['name'],
                'current_price': stock1_data.get('current_price'),
                'market_cap': stock1_data.get('market_cap'),
                'market_cap_formatted': stock1_data.get('market_cap_formatted'),
                'pe_ratio': stock1_data.get('pe_ratio'),
                'dividend_yield': stock1_data.get('dividend_yield'),
                'week_52_high': stock1_data.get('week_52_high'),
                'week_52_low': stock1_data.get('week_52_low'),
                'sector': stock1_data.get('sector'),
                'industry': stock1_data.get('industry'),
                'beta': stock1_data.get('beta'),
                'profit_margins': stock1_data.get('profit_margins'),
                'earnings_growth': stock1_data.get('earnings_growth'),
                'debt_to_equity': stock1_data.get('debt_to_equity'),
            },
            'stock2': {
                'ticker': stock2_data['ticker'],
                'name': stock2_data['name'],
                'current_price': stock2_data.get('current_price'),
                'market_cap': stock2_data.get('market_cap'),
                'market_cap_formatted': stock2_data.get('market_cap_formatted'),
                'pe_ratio': stock2_data.get('pe_ratio'),
                'dividend_yield': stock2_data.get('dividend_yield'),
                'week_52_high': stock2_data.get('week_52_high'),
                'week_52_low': stock2_data.get('week_52_low'),
                'sector': stock2_data.get('sector'),
                'industry': stock2_data.get('industry'),
                'beta': stock2_data.get('beta'),
                'profit_margins': stock2_data.get('profit_margins'),
                'earnings_growth': stock2_data.get('earnings_growth'),
                'debt_to_equity': stock2_data.get('debt_to_equity'),
            }
        }
        
        # Generate AI summary
        summary = await generate_comparison_summary(comparison)
        
        return comparison, summary
        
    except Exception as e:
        error_msg = f"Error comparing stocks: {str(e)}"
        return None, error_msg


async def generate_comparison_summary(comparison: Dict) -> str:
    """
    Generate AI-powered comparison summary.
    
    Args:
        comparison: Dictionary with stock comparison data
        
    Returns:
        AI-generated summary
    """
    try:
        stock1 = comparison['stock1']
        stock2 = comparison['stock2']
        
        # Build context
        context = build_comparison_context(stock1, stock2)
        
        # Initialize Groq client
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Build prompt
        prompt = f"""You are a financial analyst comparing two stocks. Provide a comprehensive comparison summary.

Stock 1: {stock1['name']} ({stock1['ticker']})
Stock 2: {stock2['name']} ({stock2['ticker']})

Comparison Data:
{context}

Instructions:
- Provide a 4-5 paragraph comparison covering:
  1. Overview of both companies
  2. Valuation comparison (price, market cap, P/E ratio)
  3. Financial health and performance
  4. Risk analysis (beta, volatility)
  5. Investment recommendation perspective
- Be objective and data-driven
- Highlight key differences and similarities
- Mention which might be better for different investment goals
- Keep it professional and informative

Summary:"""
        
        # Call Groq API
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert financial analyst. Provide thorough, balanced stock comparisons."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1024
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def build_comparison_context(stock1: Dict, stock2: Dict) -> str:
    """Build formatted comparison context"""
    lines = []
    
    # Price comparison
    if stock1.get('current_price') and stock2.get('current_price'):
        lines.append(f"{stock1['ticker']} Price: ${stock1['current_price']:.2f}")
        lines.append(f"{stock2['ticker']} Price: ${stock2['current_price']:.2f}")
        lines.append("")
    
    # Market cap
    if stock1.get('market_cap_formatted') and stock2.get('market_cap_formatted'):
        lines.append(f"{stock1['ticker']} Market Cap: {stock1['market_cap_formatted']}")
        lines.append(f"{stock2['ticker']} Market Cap: {stock2['market_cap_formatted']}")
        lines.append("")
    
    # Valuation
    if stock1.get('pe_ratio') and stock2.get('pe_ratio'):
        lines.append(f"{stock1['ticker']} P/E Ratio: {stock1['pe_ratio']:.2f}")
        lines.append(f"{stock2['ticker']} P/E Ratio: {stock2['pe_ratio']:.2f}")
        lines.append("")
    
    # Dividend
    if stock1.get('dividend_yield') and stock2.get('dividend_yield'):
        lines.append(f"{stock1['ticker']} Dividend Yield: {stock1['dividend_yield']*100:.2f}%")
        lines.append(f"{stock2['ticker']} Dividend Yield: {stock2['dividend_yield']*100:.2f}%")
        lines.append("")
    
    # Sector/Industry
    lines.append(f"{stock1['ticker']} Sector: {stock1.get('sector', 'N/A')}")
    lines.append(f"{stock2['ticker']} Sector: {stock2.get('sector', 'N/A')}")
    lines.append("")
    
    # Performance metrics
    if stock1.get('profit_margins') and stock2.get('profit_margins'):
        lines.append(f"{stock1['ticker']} Profit Margin: {stock1['profit_margins']*100:.2f}%")
        lines.append(f"{stock2['ticker']} Profit Margin: {stock2['profit_margins']*100:.2f}%")
        lines.append("")
    
    if stock1.get('earnings_growth') and stock2.get('earnings_growth'):
        lines.append(f"{stock1['ticker']} Earnings Growth: {stock1['earnings_growth']*100:.2f}%")
        lines.append(f"{stock2['ticker']} Earnings Growth: {stock2['earnings_growth']*100:.2f}%")
        lines.append("")
    
    # Risk
    if stock1.get('beta') and stock2.get('beta'):
        lines.append(f"{stock1['ticker']} Beta: {stock1['beta']:.2f}")
        lines.append(f"{stock2['ticker']} Beta: {stock2['beta']:.2f}")
        lines.append("")
    
    if stock1.get('debt_to_equity') and stock2.get('debt_to_equity'):
        lines.append(f"{stock1['ticker']} Debt-to-Equity: {stock1['debt_to_equity']:.2f}")
        lines.append(f"{stock2['ticker']} Debt-to-Equity: {stock2['debt_to_equity']:.2f}")
    
    return "\n".join(lines)

