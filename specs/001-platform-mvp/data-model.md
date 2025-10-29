# Data Model: Finalytics MVP Platform

## Document Control

**Created**: 2025-10-28  
**Purpose**: Define all database entities, relationships, and validation rules  
**ORM**: SQLAlchemy with Alembic migrations  
**Database**: PostgreSQL 14+

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
└────────┬────────┘
         │
         │ 1:N relationships
         ├──────────────┐
         │              │
         ▼              ▼
   ┌──────────┐   ┌─────────────┐
   │ Document │   │ StockQuery  │
   └────┬─────┘   └─────────────┘
        │
        │ 1:N
        ▼
   ┌────────────────┐
   │ QueryHistory   │
   └────────────────┘

┌──────────────────┐      ┌──────────────────┐
│   NewsArticle    │      │ StockComparison  │
└──────────────────┘      └──────────────────┘
   (independent)             (linked to User)

┌──────────────────┐
│      Export      │
└──────────────────┘
   (polymorphic: Document or StockComparison)
```

---

## Entity Definitions

### Entity: User

**Purpose**: Stores user accounts for authentication and authorization

**Table**: `users`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password (cost factor 12) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| last_login | TIMESTAMP | NULL | Last successful login timestamp |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |

**Indexes**:
- `idx_users_email` on `email` (for login queries)
- `idx_users_created_at` on `created_at` (for analytics)

**Validation Rules**:
- Email must be valid format (validated by Pydantic)
- Password must be minimum 8 characters before hashing
- Password hash must be 60 characters (bcrypt output)

**SQLAlchemy Model**:
```python
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    documents = relationship("Document", back_populates="user")
    stock_queries = relationship("StockQuery", back_populates="user")
    stock_comparisons = relationship("StockComparison", back_populates="user")
    exports = relationship("Export", back_populates="user")
```

---

### Entity: Document

**Purpose**: Tracks uploaded financial documents and their processing status

**Table**: `documents`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique document identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | Document owner |
| filename | VARCHAR(255) | NOT NULL | Original filename |
| file_size | INTEGER | NOT NULL, CHECK (file_size <= 52428800) | Size in bytes (max 50MB) |
| storage_path | VARCHAR(500) | NOT NULL, UNIQUE | Local filesystem path |
| status | ENUM | NOT NULL, DEFAULT 'uploading' | Processing status |
| page_count | INTEGER | NULL, CHECK (page_count > 0) | Number of pages (set after OCR) |
| uploaded_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Upload timestamp |
| processed_at | TIMESTAMP | NULL | When processing completed |
| error_message | TEXT | NULL | Error details if failed |

**Enums**:
- `status`: `uploading`, `processing`, `ready`, `error`

**Indexes**:
- `idx_documents_user_id` on `user_id` (for user dashboard)
- `idx_documents_status` on `status` (for filtering)
- `idx_documents_uploaded_at` on `uploaded_at` (for sorting)

**Validation Rules**:
- Filename must not be empty
- File size must be between 1 byte and 50MB
- Storage path must exist when status is not 'uploading'
- processed_at must be NULL when status is not 'ready' or 'error'
- error_message must be NULL when status is not 'error'

**SQLAlchemy Model**:
```python
import enum

class DocumentStatus(str, enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String(500), nullable=False, unique=True)
    status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.UPLOADING, index=True)
    page_count = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    
    __table_args__ = (
        CheckConstraint('file_size <= 52428800', name='check_file_size_limit'),
        CheckConstraint('page_count > 0', name='check_page_count_positive'),
    )
    
    # Relationships
    user = relationship("User", back_populates="documents")
    query_history = relationship("QueryHistory", back_populates="document")
    exports = relationship("Export", foreign_keys="Export.source_id")
```

**State Transitions**:
```
uploading → processing → ready
                     ↘ error
```

---

### Entity: QueryHistory

**Purpose**: Stores Q&A interactions between users and documents

**Table**: `query_history`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique query identifier |
| document_id | UUID | FOREIGN KEY (documents.id), NOT NULL | Related document |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | User who asked |
| question | TEXT | NOT NULL, CHECK (length(question) <= 5000) | User's question |
| answer | TEXT | NOT NULL, CHECK (length(answer) <= 10000) | RAG generated answer |
| citations | JSONB | NULL | Page references array |
| confidence | NUMERIC(3,2) | NULL, CHECK (confidence >= 0 AND confidence <= 1) | Answer confidence score |
| response_time_ms | INTEGER | NOT NULL, CHECK (response_time_ms > 0) | Processing time |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Query timestamp |

**Indexes**:
- `idx_query_history_document_id` on `document_id` (for document Q&A list)
- `idx_query_history_user_id` on `user_id` (for user history)
- `idx_query_history_created_at` on `created_at` (for sorting)

**JSONB Schema for citations**:
```json
[
  {
    "page": 15,
    "text": "Q4 2024 revenue: $42.5B",
    "chunk_id": "chunk_123"
  }
]
```

**SQLAlchemy Model**:
```python
from sqlalchemy.dialects.postgresql import JSONB

class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    citations = Column(JSONB, nullable=True)
    confidence = Column(Numeric(3, 2), nullable=True)
    response_time_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    __table_args__ = (
        CheckConstraint('length(question) <= 5000', name='check_question_length'),
        CheckConstraint('length(answer) <= 10000', name='check_answer_length'),
        CheckConstraint('confidence >= 0 AND confidence <= 1', name='check_confidence_range'),
        CheckConstraint('response_time_ms > 0', name='check_response_time_positive'),
    )
    
    # Relationships
    document = relationship("Document", back_populates="query_history")
    user = relationship("User")
```

---

### Entity: NewsArticle

**Purpose**: Stores scraped news articles from RSS feeds

**Table**: `news_articles`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique article identifier |
| title | VARCHAR(500) | NOT NULL | Article headline |
| source | ENUM | NOT NULL | News source |
| url | TEXT | NOT NULL, UNIQUE | Original article URL |
| published_at | TIMESTAMP | NOT NULL | Publication timestamp |
| summary | TEXT | NULL, CHECK (length(summary) <= 2000) | AI generated summary |
| summarized_at | TIMESTAMP | NULL | Summary creation timestamp |
| scraped_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | When we fetched it |

**Enums**:
- `source`: `cnbc`, `bbc`, `techcrunch`

**Indexes**:
- `idx_news_articles_source` on `source` (for filtering)
- `idx_news_articles_published_at` on `published_at` DESC (for chronological display)
- `idx_news_articles_url` on `url` (for deduplication)

**SQLAlchemy Model**:
```python
class NewsSource(str, enum.Enum):
    CNBC = "cnbc"
    BBC = "bbc"
    TECHCRUNCH = "techcrunch"

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    source = Column(Enum(NewsSource), nullable=False, index=True)
    url = Column(Text, nullable=False, unique=True, index=True)
    published_at = Column(DateTime(timezone=True), nullable=False, index=True)
    summary = Column(Text, nullable=True)
    summarized_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint('length(summary) <= 2000', name='check_summary_length'),
    )
```

---

### Entity: StockQuery

**Purpose**: Stores stock ticker queries and responses

**Table**: `stock_queries`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique query identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | User who queried |
| ticker | VARCHAR(5) | NOT NULL | Stock ticker symbol (uppercase) |
| question | TEXT | NOT NULL, CHECK (length(question) <= 5000) | Natural language query |
| answer | TEXT | NOT NULL, CHECK (length(answer) <= 10000) | Generated response |
| data_points | JSONB | NULL | Structured data used |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Query timestamp |

**Indexes**:
- `idx_stock_queries_user_id` on `user_id` (for user history)
- `idx_stock_queries_ticker` on `ticker` (for analytics)
- `idx_stock_queries_created_at` on `created_at` (for sorting)

**JSONB Schema for data_points**:
```json
{
  "price": 178.45,
  "pe_ratio": 29.3,
  "market_cap": 2800000000000,
  "volume": 52000000,
  "timestamp": "2025-10-28T12:00:00Z"
}
```

**SQLAlchemy Model**:
```python
class StockQuery(Base):
    __tablename__ = "stock_queries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    ticker = Column(String(5), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    data_points = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    __table_args__ = (
        CheckConstraint('length(question) <= 5000', name='check_question_length'),
        CheckConstraint('length(answer) <= 10000', name='check_answer_length'),
        CheckConstraint('ticker = UPPER(ticker)', name='check_ticker_uppercase'),
    )
    
    # Relationships
    user = relationship("User", back_populates="stock_queries")
```

---

### Entity: StockComparison

**Purpose**: Stores stock-to-stock comparisons

**Table**: `stock_comparisons`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique comparison identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | User who compared |
| ticker1 | VARCHAR(5) | NOT NULL | First stock ticker |
| ticker2 | VARCHAR(5) | NOT NULL | Second stock ticker |
| metrics | JSONB | NOT NULL | Comparison data |
| summary | TEXT | NOT NULL, CHECK (length(summary) <= 5000) | AI generated summary |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Comparison timestamp |

**Indexes**:
- `idx_stock_comparisons_user_id` on `user_id` (for user history)
- `idx_stock_comparisons_created_at` on `created_at` (for sorting)

**JSONB Schema for metrics**:
```json
{
  "ticker1": "AAPL",
  "ticker2": "MSFT",
  "price": {
    "AAPL": 178.45,
    "MSFT": 378.92,
    "difference_pct": 112.4
  },
  "market_cap": {
    "AAPL": "2.8T",
    "MSFT": "2.9T",
    "difference_pct": 3.6
  },
  "pe_ratio": {
    "AAPL": 29.3,
    "MSFT": 35.1,
    "difference_pct": 19.8
  }
}
```

**SQLAlchemy Model**:
```python
class StockComparison(Base):
    __tablename__ = "stock_comparisons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    ticker1 = Column(String(5), nullable=False)
    ticker2 = Column(String(5), nullable=False)
    metrics = Column(JSONB, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    __table_args__ = (
        CheckConstraint('length(summary) <= 5000', name='check_summary_length'),
        CheckConstraint('ticker1 != ticker2', name='check_different_tickers'),
        CheckConstraint('ticker1 = UPPER(ticker1)', name='check_ticker1_uppercase'),
        CheckConstraint('ticker2 = UPPER(ticker2)', name='check_ticker2_uppercase'),
    )
    
    # Relationships
    user = relationship("User", back_populates="stock_comparisons")
    exports = relationship("Export", foreign_keys="Export.source_id")
```

---

### Entity: Export

**Purpose**: Tracks exported analyses and files

**Table**: `exports`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique export identifier |
| user_id | UUID | FOREIGN KEY (users.id), NOT NULL | User who exported |
| source_type | ENUM | NOT NULL | What was exported |
| source_id | UUID | NOT NULL | Related entity ID |
| format | ENUM | NOT NULL | Export format |
| storage_path | VARCHAR(500) | NOT NULL, UNIQUE | File location |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Export timestamp |
| expires_at | TIMESTAMP | NOT NULL | When to delete |

**Enums**:
- `source_type`: `document`, `comparison`
- `format`: `pdf`, `docx`

**Indexes**:
- `idx_exports_user_id` on `user_id` (for user history)
- `idx_exports_expires_at` on `expires_at` (for cleanup job)
- `idx_exports_created_at` on `created_at` (for sorting)

**SQLAlchemy Model**:
```python
class ExportSourceType(str, enum.Enum):
    DOCUMENT = "document"
    COMPARISON = "comparison"

class ExportFormat(str, enum.Enum):
    PDF = "pdf"
    DOCX = "docx"

class Export(Base):
    __tablename__ = "exports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    source_type = Column(Enum(ExportSourceType), nullable=False)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    format = Column(Enum(ExportFormat), nullable=False)
    storage_path = Column(String(500), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="exports")
```

---

## Relationships Summary

| Parent | Child | Type | Cascade |
|--------|-------|------|---------|
| User | Document | One-to-Many | DELETE → CASCADE |
| User | QueryHistory | One-to-Many | DELETE → CASCADE |
| User | StockQuery | One-to-Many | DELETE → CASCADE |
| User | StockComparison | One-to-Many | DELETE → CASCADE |
| User | Export | One-to-Many | DELETE → CASCADE |
| Document | QueryHistory | One-to-Many | DELETE → CASCADE |
| Document | Export | One-to-Many | DELETE → SET NULL |
| StockComparison | Export | One-to-Many | DELETE → SET NULL |

---

## Migration Strategy

### Initial Migration (001_initial_schema.py)
```python
def upgrade():
    # Create enums
    op.execute("CREATE TYPE document_status AS ENUM ('uploading', 'processing', 'ready', 'error')")
    op.execute("CREATE TYPE news_source AS ENUM ('cnbc', 'bbc', 'techcrunch')")
    op.execute("CREATE TYPE export_source_type AS ENUM ('document', 'comparison')")
    op.execute("CREATE TYPE export_format AS ENUM ('pdf', 'docx')")
    
    # Create tables in dependency order
    op.create_table('users', ...)
    op.create_table('documents', ...)
    op.create_table('query_history', ...)
    op.create_table('news_articles', ...)
    op.create_table('stock_queries', ...)
    op.create_table('stock_comparisons', ...)
    op.create_table('exports', ...)
    
    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])
    # ... all other indexes
```

### Future Migrations
- Phase-based: One migration per implementation phase
- Backward compatible: Always support N-1 version rollback
- Data migrations: Separate from schema changes when possible
- Testing: Test against production-like data volumes

---

## Data Retention Policies

| Entity | Retention Period | Cleanup Strategy |
|--------|------------------|------------------|
| User | Indefinite | User-initiated deletion only |
| Document | 90 days of inactivity | Background job (daily) |
| QueryHistory | Tied to Document | CASCADE delete with document |
| NewsArticle | 30 days | Background job (daily) |
| StockQuery | 90 days | Background job (weekly) |
| StockComparison | 90 days | Background job (weekly) |
| Export | 24 hours | Background job (hourly) |

---

## Performance Considerations

### Query Optimization
- Use appropriate indexes for all foreign keys
- Composite indexes for common filter combinations
- EXPLAIN ANALYZE for slow queries during development
- Connection pooling (50 connections for MVP)

### Scaling Strategies
- Read replicas for analytics queries (future)
- Partitioning for time-series data (NewsArticle, QueryHistory)
- Archive old data to cold storage after retention period
- Materialized views for complex aggregations (future)

---

**Data Model Version**: 1.0  
**Last Updated**: 2025-10-28  
**Alembic Migration**: migrations/versions/001_initial_schema.py

