"""Pydantic schemas for request/response validation"""
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenData
)
from app.schemas.document import (
    DocumentUpload,
    DocumentResponse,
    DocumentQuery,
    DocumentAnswer,
    QueryHistoryResponse
)
from app.schemas.news import (
    NewsArticleResponse,
    NewsSummarizeRequest,
    NewsSummaryResponse
)
from app.schemas.export import (
    ExportRequest,
    EmailExportRequest,
    ExportResponse
)
from app.schemas.stock import (
    StockQueryRequest,
    StockDataResponse,
    StockQueryResponse,
    StockHistoryRequest,
    StockHistoryResponse,
    StockQueryHistoryResponse
)
from app.schemas.comparison import (
    ComparisonRequest,
    StockComparisonData,
    ComparisonResponse,
    ComparisonHistoryResponse
)

__all__ = [
    "UserCreate",
    "UserLogin", 
    "UserResponse",
    "Token",
    "TokenData",
    "DocumentUpload",
    "DocumentResponse",
    "DocumentQuery",
    "DocumentAnswer",
    "QueryHistoryResponse",
    "NewsArticleResponse",
    "NewsSummarizeRequest",
    "NewsSummaryResponse",
    "ExportRequest",
    "EmailExportRequest",
    "ExportResponse",
    "StockQueryRequest",
    "StockDataResponse",
    "StockQueryResponse",
    "StockHistoryRequest",
    "StockHistoryResponse",
    "StockQueryHistoryResponse",
    "ComparisonRequest",
    "StockComparisonData",
    "ComparisonResponse",
    "ComparisonHistoryResponse"
]

