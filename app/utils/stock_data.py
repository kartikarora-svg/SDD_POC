"""Yahoo Finance data fetcher"""
import yfinance as yf
from typing import Dict, Optional
from datetime import datetime


def get_stock_data(ticker: str) -> Optional[Dict]:
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with stock data or None if error
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get current price
        try:
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        except:
            current_price = None
        
        # Format market cap
        market_cap = info.get('marketCap')
        if market_cap:
            market_cap_formatted = format_large_number(market_cap)
        else:
            market_cap_formatted = 'N/A'
        
        # Compile key data
        stock_data = {
            'ticker': ticker.upper(),
            'name': info.get('longName', ticker),
            'current_price': current_price,
            'market_cap': info.get('marketCap'),
            'market_cap_formatted': market_cap_formatted,
            'pe_ratio': info.get('trailingPE') or info.get('forwardPE'),
            'dividend_yield': info.get('dividendYield'),
            'week_52_high': info.get('fiftyTwoWeekHigh'),
            'week_52_low': info.get('fiftyTwoWeekLow'),
            'volume': info.get('volume'),
            'avg_volume': info.get('averageVolume'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'description': info.get('longBusinessSummary', ''),
            'website': info.get('website'),
            'employees': info.get('fullTimeEmployees'),
            'beta': info.get('beta'),
            'revenue': info.get('totalRevenue'),
            'earnings_growth': info.get('earningsGrowth'),
            'profit_margins': info.get('profitMargins'),
            'debt_to_equity': info.get('debtToEquity'),
            'timestamp': datetime.now().isoformat()
        }
        
        return stock_data
        
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return None


def format_large_number(num: float) -> str:
    """Format large numbers (e.g., market cap) to readable format"""
    if num >= 1_000_000_000_000:  # Trillion
        return f"${num / 1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000:  # Billion
        return f"${num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:  # Million
        return f"${num / 1_000_000:.2f}M"
    else:
        return f"${num:,.2f}"


def get_stock_history(ticker: str, period: str = "1mo") -> Optional[Dict]:
    """
    Get historical stock price data.
    
    Args:
        ticker: Stock ticker symbol
        period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max')
        
    Returns:
        Dictionary with historical data or None
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return None
        
        # Convert to list of dictionaries
        history_data = []
        for index, row in hist.iterrows():
            history_data.append({
                'date': index.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
        
        return {
            'ticker': ticker.upper(),
            'period': period,
            'data': history_data
        }
        
    except Exception as e:
        print(f"Error fetching stock history for {ticker}: {e}")
        return None

