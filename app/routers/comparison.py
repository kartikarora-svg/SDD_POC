"""Stock comparison API endpoints"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models.user import User
from app.models.comparison import StockComparison
from app.schemas.comparison import (
    ComparisonRequest,
    ComparisonResponse,
    ComparisonHistoryResponse
)
from app.utils.auth import get_current_user
from app.utils.stock_comparator import compare_stocks

router = APIRouter()


async def _compare_stocks_impl(
    comparison_request: ComparisonRequest,
    current_user: User,
    db: Session
):
    """
    Compare two stocks side-by-side with AI analysis.
    
    - **ticker1**: First stock ticker symbol
    - **ticker2**: Second stock ticker symbol
    
    Returns detailed comparison with AI-generated summary.
    """
    ticker1 = comparison_request.ticker1.upper()
    ticker2 = comparison_request.ticker2.upper()
    
    # Validate different tickers
    if ticker1 == ticker2:
        raise HTTPException(
            status_code=400,
            detail="Please provide two different ticker symbols"
        )
    
    # Compare stocks
    comparison_data, ai_summary = await compare_stocks(ticker1, ticker2)
    
    if not comparison_data:
        raise HTTPException(
            status_code=400,
            detail=ai_summary or "Could not compare stocks"
        )
    
    # Save comparison
    comparison_record = StockComparison(
        user_id=str(current_user.id),
        ticker1=ticker1,
        ticker2=ticker2,
        comparison_data=json.dumps(comparison_data),
        ai_summary=ai_summary
    )
    
    db.add(comparison_record)
    db.commit()
    db.refresh(comparison_record)
    
    # Format response
    return {
        "comparison_id": str(comparison_record.id),
        "stock1": comparison_data['stock1'],
        "stock2": comparison_data['stock2'],
        "ai_summary": ai_summary,
        "created_at": comparison_record.created_at
    }


@router.post("/", response_model=ComparisonResponse)
async def compare_stocks_endpoint_slash(
    comparison_request: ComparisonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two stocks (with trailing slash)."""
    return await _compare_stocks_impl(comparison_request, current_user, db)


@router.post("", response_model=ComparisonResponse)
async def compare_stocks_endpoint_no_slash(
    comparison_request: ComparisonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare two stocks (without trailing slash)."""
    return await _compare_stocks_impl(comparison_request, current_user, db)


@router.get("/history", response_model=List[ComparisonHistoryResponse])
async def get_comparison_history(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's stock comparison history.
    
    - **limit**: Maximum number of comparisons to return
    
    Returns list of previous comparisons.
    """
    comparisons = db.query(StockComparison).filter(
        StockComparison.user_id == str(current_user.id)
    ).order_by(desc(StockComparison.created_at)).limit(limit).all()
    
    return comparisons


@router.get("/{comparison_id}")
async def get_comparison_detail(
    comparison_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed comparison by ID.
    
    - **comparison_id**: ID of the comparison
    
    Returns full comparison data.
    """
    comparison = db.query(StockComparison).filter(
        StockComparison.id == comparison_id,
        StockComparison.user_id == str(current_user.id)
    ).first()
    
    if not comparison:
        raise HTTPException(
            status_code=404,
            detail="Comparison not found"
        )
    
    # Parse comparison data
    comparison_data = json.loads(comparison.comparison_data)
    
    return {
        "comparison_id": str(comparison.id),
        "stock1": comparison_data['stock1'],
        "stock2": comparison_data['stock2'],
        "ai_summary": comparison.ai_summary,
        "created_at": comparison.created_at
    }

