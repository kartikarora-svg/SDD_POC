"""Stock comparison schemas"""
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, Field


class ComparisonRequest(BaseModel):
    """Schema for stock comparison request"""
    ticker1: str = Field(..., description="First stock ticker")
    ticker2: str = Field(..., description="Second stock ticker")


class StockComparisonData(BaseModel):
    """Schema for individual stock data in comparison"""
    ticker: str
    name: str
    current_price: float | None = None
    market_cap_formatted: str | None = None
    pe_ratio: float | None = None
    dividend_yield: float | None = None
    sector: str | None = None
    industry: str | None = None
    beta: float | None = None
    profit_margins: float | None = None
    earnings_growth: float | None = None


class ComparisonResponse(BaseModel):
    """Schema for comparison response"""
    comparison_id: str
    stock1: StockComparisonData
    stock2: StockComparisonData
    ai_summary: str
    created_at: datetime


class ComparisonHistoryResponse(BaseModel):
    """Schema for comparison history"""
    id: str
    ticker1: str
    ticker2: str
    ai_summary: str
    created_at: datetime
    
    class Config:
        from_attributes = True

