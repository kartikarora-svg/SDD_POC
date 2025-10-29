"""Stock intelligence API endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.user import User
from app.models.stock import StockQuery
from app.schemas.stock import (
    StockQueryRequest,
    StockQueryResponse,
    StockHistoryRequest,
    StockHistoryResponse,
    StockQueryHistoryResponse
)
from app.utils.auth import get_current_user
from app.utils.stock_data import get_stock_data, get_stock_history
from app.utils.stock_rag import query_stock

router = APIRouter()


@router.post("/query", response_model=StockQueryResponse)
async def query_stock_endpoint(
    query_request: StockQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ask a question about a stock using natural language.
    
    - **ticker**: Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
    - **question**: Your question about the stock
    
    Returns AI-generated answer based on real-time Yahoo Finance data.
    """
    ticker = query_request.ticker.upper()
    question = query_request.question
    
    # Query stock using RAG
    answer, stock_data = await query_stock(ticker, question)
    
    if not stock_data:
        raise HTTPException(
            status_code=400,
            detail=f"Could not fetch data for ticker '{ticker}'"
        )
    
    # Save query history
    stock_query = StockQuery(
        user_id=str(current_user.id),
        ticker=ticker,
        question=question,
        answer=answer,
        current_price=stock_data.get('current_price'),
        market_cap=stock_data.get('market_cap')
    )
    
    db.add(stock_query)
    db.commit()
    
    # Format stock data for response
    stock_data_response = {
        'ticker': stock_data['ticker'],
        'name': stock_data['name'],
        'current_price': stock_data.get('current_price'),
        'market_cap_formatted': stock_data.get('market_cap_formatted'),
        'pe_ratio': stock_data.get('pe_ratio'),
        'dividend_yield': stock_data.get('dividend_yield'),
        'week_52_high': stock_data.get('week_52_high'),
        'week_52_low': stock_data.get('week_52_low'),
        'sector': stock_data.get('sector'),
        'industry': stock_data.get('industry')
    }
    
    return {
        "ticker": ticker,
        "question": question,
        "answer": answer,
        "stock_data": stock_data_response
    }


@router.get("/data/{ticker}")
async def get_stock_data_endpoint(
    ticker: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get current stock data for a ticker.
    
    - **ticker**: Stock ticker symbol
    
    Returns real-time data from Yahoo Finance.
    """
    ticker = ticker.upper()
    stock_data = get_stock_data(ticker)
    
    if not stock_data:
        raise HTTPException(
            status_code=404,
            detail=f"Could not fetch data for ticker '{ticker}'"
        )
    
    return stock_data


@router.post("/history", response_model=StockHistoryResponse)
async def get_stock_history_endpoint(
    history_request: StockHistoryRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Get historical price data for a stock.
    
    - **ticker**: Stock ticker symbol
    - **period**: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max')
    
    Returns historical price data.
    """
    ticker = history_request.ticker.upper()
    period = history_request.period
    
    history_data = get_stock_history(ticker, period)
    
    if not history_data:
        raise HTTPException(
            status_code=404,
            detail=f"Could not fetch history for ticker '{ticker}'"
        )
    
    return history_data


@router.get("/history/queries", response_model=List[StockQueryHistoryResponse])
async def get_query_history(
    ticker: str = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's stock query history.
    
    - **ticker**: Optional ticker filter
    - **limit**: Maximum number of queries to return
    
    Returns list of previous stock queries.
    """
    query = db.query(StockQuery).filter(
        StockQuery.user_id == str(current_user.id)
    )
    
    if ticker:
        query = query.filter(StockQuery.ticker == ticker.upper())
    
    queries = query.order_by(desc(StockQuery.created_at)).limit(limit).all()
    
    return queries

