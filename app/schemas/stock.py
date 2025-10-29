"""Stock-related Pydantic schemas"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class StockQueryRequest(BaseModel):
    """Schema for stock query request"""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT)")
    question: str = Field(..., min_length=3, description="Question about the stock")


class StockDataResponse(BaseModel):
    """Schema for stock data response"""
    ticker: str
    name: str
    current_price: Optional[float] = None
    market_cap_formatted: Optional[str] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class StockQueryResponse(BaseModel):
    """Schema for stock query answer"""
    ticker: str
    question: str
    answer: str
    stock_data: Optional[StockDataResponse] = None


class StockHistoryRequest(BaseModel):
    """Schema for stock history request"""
    ticker: str
    period: str = Field(default="1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max")


class StockHistoryResponse(BaseModel):
    """Schema for stock history response"""
    ticker: str
    period: str
    data: List[Dict]


class StockQueryHistoryResponse(BaseModel):
    """Schema for stock query history"""
    id: str
    ticker: str
    question: str
    answer: str
    current_price: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

