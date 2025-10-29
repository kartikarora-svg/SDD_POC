# Technical Specification: Finalytics MVP Platform

## Document Control

- **Version**: 1.0
- **Status**: Draft
- **Created**: 2025-10-28
- **Last Updated**: 2025-10-28
- **Owner**: Finalytics Team
- **Reviewers**: TBD

## Executive Summary

The Finalytics MVP Platform is a comprehensive web-based financial analytics application that implements all five constitutional principles in a streamlined, efficient architecture. This specification defines a minimum viable product that delivers intelligent document analysis, real-time market data, live news feeds, and comparative stock analysis through a simple yet powerful interface.

The platform uses a FastAPI backend to provide RESTful endpoints for all core functionality, paired with a vanilla HTML, CSS, and JavaScript frontend that delivers a responsive, fast user experience without framework overhead. This approach prioritizes simplicity, maintainability, and rapid development while satisfying all constitutional requirements.

Users will be able to upload financial documents for AI-powered Q&A, export their analyses, browse live financial news with AI summaries, query real-time stock data through natural language, and compare stocks side-by-side—all through an intuitive web interface that works seamlessly across desktop and mobile devices.


## Constitutional Alignment

This specification upholds all five Finalytics constitutional principles:

- **Principle 1: On-Demand Document Intelligence**
  - **How**: FastAPI endpoints handle PDF uploads, trigger OCR processing, and establish document-scoped RAG agents. Frontend provides upload interface and real-time Q&A chat.
  - **Validation**: Users can upload a 10-K PDF and receive answers to natural language questions within 30 seconds.

- **Principle 2: Actionable & Shareable Analysis**
  - **How**: Export endpoints generate PDF and DOCX files from analysis sessions. Email endpoint sends formatted reports via SMTP. Frontend provides clearly labeled export buttons.
  - **Validation**: Users can click export buttons and receive properly formatted documents preserving all content and context.

- **Principle 3: Real-Time Market Awareness**
  - **How**: Backend scraper fetches news from financial sources every 5 minutes. AI summarization endpoint processes articles on-demand. Frontend displays scrolling news feed with click-to-summarize functionality.
  - **Validation**: News feed updates within 5 minutes of new articles appearing on source sites. Summaries generate within 2 seconds of user click.

- **Principle 4: Live Ticker RAG Agent**
  - **How**: Yahoo Finance RAG agent endpoint wraps yfinance library with conversational AI. Frontend provides ticker input and chat interface for natural language queries.
  - **Validation**: Users enter a ticker symbol, ask questions in plain English, and receive accurate real-time market data responses.

- **Principle 5: Seamless Comparative Analysis**
  - **How**: Comparison endpoint accepts two tickers, fetches data via yfinance, performs side-by-side analysis, and generates AI summary. Frontend displays comparison table and insights.
  - **Validation**: Users input two ticker symbols and receive a formatted comparison with key metrics and AI-generated insights.

## Scope

### In Scope

- **Document Analysis (Principle 1)**
  - PDF upload interface with drag-and-drop support
  - OCR and text extraction for scanned documents
  - Document-scoped RAG agent setup and management
  - Real-time Q&A chat interface for uploaded documents
  - Document history and session management

- **Export & Sharing (Principle 2)**
  - PDF export of analysis sessions with formatting
  - DOCX export with proper structure and styling
  - Email sharing with attachment or inline content
  - Export history and download management

- **News Feed (Principle 3)**
  - Automated news scraping from CNBC, BBC, TechCrunch
  - Live-updating news feed display
  - On-demand AI summarization of articles
  - Source attribution and original article links
  - News feed filtering and sorting

- **Stock Ticker Agent (Principle 4)**
  - Yahoo Finance integration via yfinance
  - Natural language query processing
  - Real-time stock data retrieval
  - Conversational chat interface for stock queries
  - Query history and context retention

- **Stock Comparison (Principle 5)**
  - Two-ticker comparison interface
  - Side-by-side metric display
  - AI-generated comparison summary
  - Export of comparison results
  - Comparison history

- **Core Platform Features**
  - User authentication and session management
  - Responsive design for desktop and mobile
  - Error handling and user feedback
  - Basic user profile management
  - Activity logging and audit trail

### Out of Scope

- **Phase 1 Exclusions** (Future Enhancements)
  - Multi-user collaboration and sharing
  - Advanced portfolio tracking and management
  - Real-time WebSocket notifications
  - Mobile native applications (iOS/Android)
  - Advanced analytics and charting
  - Integration with trading platforms
  - Multi-document comparison and analysis
  - Custom news source configuration
  - Scheduled reports and alerts
  - Social features and community discussions
  - Advanced user roles and permissions
  - White-label or multi-tenant capabilities
  - API access for third-party integrations

### Future Considerations

- Portfolio management module with tracking and alerts
- Advanced visualization with interactive charts
- WebSocket-based real-time updates for news and prices
- Integration with brokerage APIs for live trading
- Mobile apps with offline capabilities
- Collaborative workspaces for team analysis
- Custom AI model fine-tuning for domain-specific queries
- Enterprise features (SSO, RBAC, audit logs)

## Requirements

### Functional Requirements

| ID | Requirement | Priority | Principle |
|----|-------------|----------|-----------|
| FR-1 | System shall accept PDF uploads up to 50MB including scanned documents | Must | P1 |
| FR-2 | System shall extract text from PDFs using OCR within 30 seconds | Must | P1 |
| FR-3 | System shall create document-scoped RAG agent immediately after upload | Must | P1 |
| FR-4 | System shall respond to natural language questions about uploaded documents | Must | P1 |
| FR-5 | System shall maintain separate RAG contexts for each uploaded document | Must | P1 |
| FR-6 | System shall provide PDF export button generating formatted analysis reports | Must | P2 |
| FR-7 | System shall provide DOCX export button generating Word-compatible documents | Must | P2 |
| FR-8 | System shall provide email sharing with inline or attachment options | Must | P2 |
| FR-9 | System shall preserve all formatting, citations, and context when exporting | Must | P2 |
| FR-10 | System shall scrape news from CNBC, BBC, and TechCrunch sources | Must | P3 |
| FR-11 | System shall update news feed at minimum every 5 minutes | Must | P3 |
| FR-12 | System shall generate AI summaries of news articles on user click | Must | P3 |
| FR-13 | System shall display source attribution and links for all news items | Must | P3 |
| FR-14 | System shall accept stock ticker symbols as input | Must | P4 |
| FR-15 | System shall respond to natural language queries about stocks using yfinance | Must | P4 |
| FR-16 | System shall provide real-time stock prices, metrics, and performance data | Must | P4 |
| FR-17 | System shall handle invalid tickers with clear error messages | Must | P4 |
| FR-18 | System shall accept two stock tickers for comparison | Must | P5 |
| FR-19 | System shall display side-by-side comparison of key stock metrics | Must | P5 |
| FR-20 | System shall generate AI summary highlighting key differences between stocks | Must | P5 |
| FR-21 | System shall allow export of comparison results via Principle 2 mechanisms | Must | P5 |
| FR-22 | System shall require user authentication for all features | Must | All |
| FR-23 | System shall provide responsive interface working on desktop and mobile | Must | All |
| FR-24 | System shall maintain user session and document history | Should | P1 |
| FR-25 | System shall allow filtering and sorting of news feed | Should | P3 |
| FR-26 | System shall retain chat history for stock queries within session | Should | P4 |
| FR-27 | System shall store comparison history for quick reference | Should | P5 |

### Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Performance: Document processing time | < 30 seconds for 100-page PDF | Time from upload to first Q&A response |
| NFR-2 | Performance: Q&A response time | < 3 seconds per query | API response time measurement |
| NFR-3 | Performance: News summarization | < 2 seconds per article | Time from click to summary display |
| NFR-4 | Performance: Stock query response | < 1 second for real-time data | API response time measurement |
| NFR-5 | Accuracy: OCR accuracy rate | > 95% on standard financial docs | Manual verification sampling |
| NFR-6 | Availability: News feed freshness | Updates every 5 minutes maximum | Timestamp comparison |
| NFR-7 | Availability: System uptime | 99% during business hours | Uptime monitoring |
| NFR-8 | Security: User authentication | JWT-based with secure storage | Security audit |
| NFR-9 | Security: Data encryption at rest | AES-256 for stored documents | Configuration verification |
| NFR-10 | Security: HTTPS enforcement | All connections over TLS 1.2+ | SSL certificate validation |
| NFR-11 | Usability: Mobile responsiveness | Works on screens 320px+ wide | Device testing |
| NFR-12 | Usability: Error messaging | All errors have clear user guidance | User testing |
| NFR-13 | Accessibility: WCAG compliance | Meets WCAG 2.1 AA standard | Automated + manual testing |
| NFR-14 | Scalability: Concurrent users | Support 100 simultaneous users | Load testing |
| NFR-15 | Scalability: Document storage | Handle 10,000 documents per user | Storage testing |

## User Stories

### Story 1: Financial Analyst - Document Q&A

**As a** financial analyst  
**I want** to upload a 10-K filing and ask questions about specific financial metrics  
**So that** I can quickly extract insights without reading the entire 200-page document

**Acceptance Criteria**:
- [ ] Given I'm logged in, when I drag and drop a PDF onto the upload area, then the system accepts it and begins processing
- [ ] Given a document is processing, when OCR completes, then I see a "Ready for Q&A" indicator within 30 seconds
- [ ] Given a document is ready, when I type "What was the revenue growth in Q4?", then I receive an accurate answer with page citations within 3 seconds
- [ ] Given I have multiple documents, when I select a different document, then my questions are answered from only that document's context

**Constitutional Compliance**: Principle 1 (On-Demand Document Intelligence)

### Story 2: Investment Advisor - Share Analysis

**As an** investment advisor  
**I want** to export my analysis of a client's 10-K document as a PDF  
**So that** I can email it to the client for their review

**Acceptance Criteria**:
- [ ] Given I have completed a Q&A session, when I click "Export to PDF", then a formatted PDF downloads with all questions, answers, and citations
- [ ] Given I want to share immediately, when I click "Email this Analysis", then a modal opens with recipient fields
- [ ] Given I enter an email address and click Send, when the email delivers, then the recipient receives a professional-looking report with my analysis
- [ ] Given I export to DOCX, when I open it in Microsoft Word, then all formatting and structure are preserved

**Constitutional Compliance**: Principle 2 (Actionable & Shareable Analysis)

### Story 3: Day Trader - Market News Monitoring

**As a** day trader  
**I want** to monitor breaking financial news with AI summaries  
**So that** I can quickly understand market-moving events without reading full articles

**Acceptance Criteria**:
- [ ] Given I'm on the news feed page, when new articles are published, then they appear in my feed within 5 minutes
- [ ] Given I see a headline, when I click on it, then an AI-generated summary appears within 2 seconds highlighting the key points
- [ ] Given I want more detail, when I click "Read Full Article", then the original source opens in a new tab
- [ ] Given I want focused news, when I filter by source or topic, then only matching articles display

**Constitutional Compliance**: Principle 3 (Real-Time Market Awareness)

### Story 4: Retail Investor - Stock Research

**As a** retail investor  
**I want** to ask natural language questions about a stock  
**So that** I can get real-time data without learning complex APIs or interfaces

**Acceptance Criteria**:
- [ ] Given I'm on the Stock Agent page, when I enter "AAPL" and ask "What's the current price?", then I receive the real-time price within 1 second
- [ ] Given I want more detail, when I ask "What's the P/E ratio and how does it compare to historical average?", then I receive accurate metrics with context
- [ ] Given I enter an invalid ticker, when I ask a question, then I receive a friendly error message explaining the ticker wasn't found
- [ ] Given I have a conversation history, when I ask follow-up questions, then the system maintains context from previous queries

**Constitutional Compliance**: Principle 4 (Live Ticker RAG Agent)

### Story 5: Portfolio Manager - Stock Comparison

**As a** portfolio manager  
**I want** to compare two technology stocks side-by-side  
**So that** I can make informed decisions about which to include in my portfolio

**Acceptance Criteria**:
- [ ] Given I'm on the Stock Comparator page, when I enter "MSFT" and "GOOGL", then I see a detailed comparison table within 2 seconds
- [ ] Given the comparison displays, when I review the metrics, then I see price, market cap, P/E ratio, 52-week performance, and other key indicators
- [ ] Given I want insights, when I scroll to the AI summary section, then I see a paragraph highlighting the most significant differences
- [ ] Given I want to save this analysis, when I click "Export Comparison", then I can save it as PDF or DOCX per Principle 2

**Constitutional Compliance**: Principle 5 (Seamless Comparative Analysis)

### Story 6: New User - Account Setup

**As a** new user  
**I want** to create an account and log in securely  
**So that** my documents and analysis history are protected and accessible only to me

**Acceptance Criteria**:
- [ ] Given I'm a new visitor, when I click "Sign Up", then I see a registration form asking for email and password
- [ ] Given I submit valid credentials, when registration completes, then I'm automatically logged in and see the dashboard
- [ ] Given I return later, when I log in with my credentials, then I see my previous documents and analysis history
- [ ] Given I'm logged in, when my session expires, then I'm redirected to login with a clear message

**Constitutional Compliance**: All principles (security requirement)

## System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │   Upload   │  │    News    │  │   Stock    │  │  Compare │ │
│  │   UI       │  │   Feed UI  │  │  Agent UI  │  │   UI     │ │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └─────┬────┘ │
│         │                │                │               │      │
│         └────────────────┴────────────────┴───────────────┘      │
│                          │ REST API Calls                        │
│                          │ (vanilla JS fetch)                    │
└──────────────────────────┼───────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────┐
│                    FastAPI Backend                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     API Router Layer                         │ │
│  │  /api/documents  /api/export  /api/news  /api/stocks       │ │
│  └───┬─────────────┬───────────┬──────────────┬───────────────┘ │
│      │             │           │              │                  │
│  ┌───▼──────┐  ┌──▼──────┐ ┌──▼────────┐  ┌──▼────────────┐   │
│  │ Document │  │ Export  │ │   News    │  │ Yahoo Finance │   │
│  │  Service │  │ Service │ │  Service  │  │   Service     │   │
│  │          │  │         │ │           │  │               │   │
│  │ - OCR    │  │ - PDF   │ │ - Scraper │  │ - yfinance    │   │
│  │ - RAG    │  │ - DOCX  │ │ - AI Sum  │  │ - RAG Agent   │   │
│  │ - Q&A    │  │ - Email │ │ - Cache   │  │ - Comparison  │   │
│  └───┬──────┘  └─────────┘ └───────────┘  └───────────────┘   │
│      │                                                           │
│  ┌───▼───────────────────────────────────────────────────────┐ │
│  │              Shared Components                             │ │
│  │  • LLM Provider (Groq)                                    │ │
│  │  • Vector Store (ChromaDB)                                │ │
│  │  • PDF Processor (Poppler/PyPDF)                          │ │
│  │  • Authentication (JWT)                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           │                                       │
└───────────────────────────┼───────────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────────┐
│                    Data Layer                                      │
│  ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌─────────────┐ │
│  │PostgreSQL│   │   Redis   │   │ Local FS │   │  ChromaDB   │ │
│  │          │   │           │   │          │   │             │ │
│  │ - Users  │   │ - Session │   │ - PDFs   │   │ - Vectors   │ │
│  │ - Docs   │   │ - Cache   │   │ - Exports│   │ - Embeddings│ │
│  │ - History│   │ - Tasks   │   │          │   │             │ │
│  └──────────┘   └───────────┘   └──────────┘   └─────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### Data Flow

#### Flow 1: Document Upload and Q&A (Principle 1)

1. User selects PDF file in browser and clicks upload
2. Frontend sends multipart form POST to `/api/documents/upload`
3. FastAPI receives file, validates size/type, stores in local filesystem
4. Document service triggers OCR pipeline (Poppler/PyPDF) for text extraction
5. Extracted text is chunked and embedded using LLM embedding model
6. Vector embeddings stored in ChromaDB with document ID as namespace
7. RAG agent initialized with document-specific retriever
8. Backend returns document ID and "ready" status to frontend
9. User types question in chat interface
10. Frontend sends POST to `/api/documents/{doc_id}/query` with question text
11. RAG agent retrieves relevant chunks from ChromaDB for that document
12. LLM generates answer using retrieved context
13. Answer returned to frontend with citations (page numbers)
14. Frontend displays answer in chat bubble

#### Flow 2: Analysis Export (Principle 2)

1. User clicks "Export to PDF" button
2. Frontend sends POST to `/api/export/pdf` with session/document ID
3. Export service retrieves chat history from database
4. Service generates HTML template with questions, answers, and metadata
5. HTML converted to PDF using library (WeasyPrint/ReportLab)
6. PDF stored temporarily in local filesystem
7. Backend returns download URL to frontend
8. Frontend triggers browser download of PDF file
9. For email: same flow but PDF attached to email via SMTP service

#### Flow 3: News Feed with Summarization (Principle 3)

1. Background scheduler runs every 5 minutes
2. News service fetches articles from CNBC, BBC, TechCrunch RSS feeds
3. New articles stored in PostgreSQL with source, timestamp, URL
4. Articles cached in Redis for fast retrieval
5. When user loads news page, frontend fetches `/api/news/feed?limit=50`
6. Backend returns latest articles from cache/database
7. Frontend renders scrolling news feed
8. User clicks headline to see summary
9. Frontend sends GET to `/api/news/{article_id}/summarize`
10. If summary exists in cache, return immediately
11. Otherwise, fetch full article content from RSS feed or original URL
12. LLM (Groq) generates concise summary (3-5 sentences)
13. Summary cached and returned to frontend
14. Frontend displays summary in modal or expanded view

#### Flow 4: Stock Ticker Q&A (Principle 4)

1. User enters ticker "TSLA" and asks "What's the current stock price?"
2. Frontend sends POST to `/api/stocks/query` with ticker and question
3. Yahoo Finance service validates ticker using yfinance
4. If valid, service fetches real-time data (price, volume, metrics)
5. Data formatted into context for LLM
6. RAG agent processes natural language question with market data context
7. LLM generates conversational response with data points
8. Response returned to frontend with metadata (timestamp, source)
9. Frontend displays answer in chat interface
10. Follow-up questions maintain context within session

#### Flow 5: Stock Comparison (Principle 5)

1. User enters "AAPL" and "MSFT" in comparison form
2. Frontend sends POST to `/api/stocks/compare` with both tickers
3. Yahoo Finance service fetches data for both stocks in parallel
4. Service extracts key metrics: price, market cap, P/E, volume, 52-week range
5. Comparison table generated with side-by-side values
6. Difference calculations performed (percentage, absolute)
7. Comparison data sent to LLM with prompt for summary generation
8. LLM generates 2-3 paragraph summary highlighting key differences
9. Table and summary returned to frontend as JSON
10. Frontend renders comparison table and summary text
11. User can click export to save as PDF/DOCX via Principle 2 flow

### API Contracts

#### Endpoint: POST /api/auth/register

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "user_id": "uuid-string",
    "email": "user@example.com",
    "token": "jwt-token-string"
  }
}
```

**Error Codes**:
- `400`: Invalid email format or weak password
- `409`: Email already registered
- `500`: Server error during registration

#### Endpoint: POST /api/auth/login

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "token": "jwt-token-string",
    "expires_at": "2025-10-29T12:00:00Z"
  }
}
```

**Error Codes**:
- `401`: Invalid credentials
- `500`: Server error

#### Endpoint: POST /api/documents/upload

**Request** (multipart/form-data):
```
file: [PDF binary data]
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "document_id": "doc-uuid",
    "filename": "10k-report.pdf",
    "status": "processing",
    "estimated_ready_time": "2025-10-28T12:01:00Z"
  }
}
```

**Error Codes**:
- `400`: File too large or invalid format
- `401`: Unauthorized
- `413`: File size exceeds 50MB limit
- `500`: Processing error

#### Endpoint: GET /api/documents/{document_id}/status

**Response**:
```json
{
  "status": "success",
  "data": {
    "document_id": "doc-uuid",
    "status": "ready",
    "page_count": 156,
    "processing_time_seconds": 24
  }
}
```

#### Endpoint: POST /api/documents/{document_id}/query

**Request**:
```json
{
  "question": "What was the total revenue in Q4 2024?"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "answer": "The total revenue in Q4 2024 was $42.5 billion, representing a 12% increase year-over-year.",
    "citations": [
      {"page": 15, "text": "Q4 2024 revenue: $42.5B"},
      {"page": 18, "text": "YoY growth: 12%"}
    ],
    "confidence": 0.95,
    "response_time_ms": 1847
  }
}
```

**Error Codes**:
- `400`: Empty question
- `401`: Unauthorized
- `404`: Document not found
- `500`: RAG processing error

#### Endpoint: POST /api/export/pdf

**Request**:
```json
{
  "document_id": "doc-uuid",
  "include_citations": true
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "download_url": "/api/export/download/export-uuid.pdf",
    "expires_at": "2025-10-28T13:00:00Z"
  }
}
```

#### Endpoint: POST /api/export/email

**Request**:
```json
{
  "document_id": "doc-uuid",
  "recipient_email": "client@example.com",
  "subject": "10-K Analysis Report",
  "format": "pdf"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "message": "Email sent successfully",
    "sent_at": "2025-10-28T12:05:00Z"
  }
}
```

**Error Codes**:
- `400`: Invalid email address
- `401`: Unauthorized
- `500`: Email service error

#### Endpoint: GET /api/news/feed

**Query Parameters**:
- `limit`: Number of articles (default: 50, max: 100)
- `source`: Filter by source (cnbc, bbc, techcrunch)
- `since`: ISO timestamp for articles after this time

**Response**:
```json
{
  "status": "success",
  "data": {
    "articles": [
      {
        "article_id": "news-uuid",
        "title": "Tech Stocks Rally on Strong Earnings",
        "source": "cnbc",
        "published_at": "2025-10-28T11:45:00Z",
        "url": "https://cnbc.com/article...",
        "has_summary": false
      }
    ],
    "total": 50,
    "updated_at": "2025-10-28T11:50:00Z"
  }
}
```

#### Endpoint: GET /api/news/{article_id}/summarize

**Response**:
```json
{
  "status": "success",
  "data": {
    "article_id": "news-uuid",
    "summary": "Technology stocks surged today following better-than-expected earnings from major companies. Apple and Microsoft both exceeded analyst predictions, driving the NASDAQ up 2.3%. Market sentiment remains positive heading into the final quarter of 2025.",
    "key_points": [
      "Tech stocks up significantly",
      "Apple and Microsoft beat earnings",
      "NASDAQ gains 2.3%"
    ],
    "generated_at": "2025-10-28T12:00:00Z"
  }
}
```

**Error Codes**:
- `404`: Article not found
- `500`: Summarization error

#### Endpoint: POST /api/stocks/query

**Request**:
```json
{
  "ticker": "AAPL",
  "question": "What's the current stock price and P/E ratio?"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "ticker": "AAPL",
    "answer": "Apple (AAPL) is currently trading at $178.45. The P/E ratio is 29.3, which is slightly above the technology sector average of 27.8.",
    "data_points": {
      "price": 178.45,
      "pe_ratio": 29.3,
      "sector_avg_pe": 27.8
    },
    "timestamp": "2025-10-28T12:00:00Z"
  }
}
```

**Error Codes**:
- `400`: Invalid ticker format
- `404`: Ticker not found
- `500`: Data fetch error

#### Endpoint: POST /api/stocks/compare

**Request**:
```json
{
  "ticker1": "AAPL",
  "ticker2": "MSFT"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "comparison": {
      "ticker1": "AAPL",
      "ticker2": "MSFT",
      "metrics": {
        "price": {"AAPL": 178.45, "MSFT": 378.92, "difference_pct": 112.4},
        "market_cap": {"AAPL": "2.8T", "MSFT": "2.9T", "difference_pct": 3.6},
        "pe_ratio": {"AAPL": 29.3, "MSFT": 35.1, "difference_pct": 19.8},
        "52_week_change": {"AAPL": "+22.5%", "MSFT": "+31.2%"}
      }
    },
    "summary": "Microsoft currently has a higher stock price and P/E ratio compared to Apple, suggesting the market expects stronger growth. However, both companies have similar market capitalizations around $2.8-2.9 trillion. Microsoft has outperformed Apple year-to-date with a 31.2% gain versus Apple's 22.5% increase.",
    "generated_at": "2025-10-28T12:00:00Z"
  }
}
```

**Error Codes**:
- `400`: Invalid tickers or same ticker entered twice
- `404`: One or both tickers not found
- `500`: Comparison processing error

## Data Model

### Entity: User

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique user identifier | Primary key |
| email | String | Yes | User email address | Unique, valid email format |
| password_hash | String | Yes | Bcrypt hashed password | Min 60 chars |
| created_at | Timestamp | Yes | Account creation time | ISO 8601 |
| last_login | Timestamp | No | Last successful login | ISO 8601 |
| is_active | Boolean | Yes | Account active status | Default true |

### Entity: Document

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique document identifier | Primary key |
| user_id | UUID | Yes | Owner user ID | Foreign key to User |
| filename | String | Yes | Original filename | Max 255 chars |
| file_size | Integer | Yes | Size in bytes | Max 52428800 (50MB) |
| storage_path | String | Yes | Blob storage path | Unique |
| status | Enum | Yes | Processing status | 'uploading', 'processing', 'ready', 'error' |
| page_count | Integer | No | Number of pages | Positive integer |
| uploaded_at | Timestamp | Yes | Upload time | ISO 8601 |
| processed_at | Timestamp | No | Ready time | ISO 8601 |
| error_message | String | No | Error details if failed | Max 1000 chars |

### Entity: QueryHistory

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique query identifier | Primary key |
| document_id | UUID | Yes | Related document | Foreign key to Document |
| user_id | UUID | Yes | User who asked | Foreign key to User |
| question | Text | Yes | User's question | Max 5000 chars |
| answer | Text | Yes | RAG generated answer | Max 10000 chars |
| citations | JSON | No | Page references | Array of objects |
| confidence | Float | No | Answer confidence | 0.0 to 1.0 |
| response_time_ms | Integer | Yes | Processing time | Positive integer |
| created_at | Timestamp | Yes | Query time | ISO 8601 |

### Entity: NewsArticle

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique article identifier | Primary key |
| title | String | Yes | Article headline | Max 500 chars |
| source | Enum | Yes | News source | 'cnbc', 'bbc', 'techcrunch' |
| url | String | Yes | Original article URL | Valid URL, unique |
| published_at | Timestamp | Yes | Publication time | ISO 8601 |
| summary | Text | No | AI generated summary | Max 2000 chars |
| summarized_at | Timestamp | No | Summary creation time | ISO 8601 |
| scraped_at | Timestamp | Yes | When we fetched it | ISO 8601 |

### Entity: StockQuery

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique query identifier | Primary key |
| user_id | UUID | Yes | User who queried | Foreign key to User |
| ticker | String | Yes | Stock ticker symbol | 1-5 uppercase chars |
| question | Text | Yes | Natural language query | Max 5000 chars |
| answer | Text | Yes | Generated response | Max 10000 chars |
| data_points | JSON | No | Structured data used | Object |
| created_at | Timestamp | Yes | Query time | ISO 8601 |

### Entity: StockComparison

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique comparison ID | Primary key |
| user_id | UUID | Yes | User who compared | Foreign key to User |
| ticker1 | String | Yes | First stock ticker | 1-5 uppercase chars |
| ticker2 | String | Yes | Second stock ticker | 1-5 uppercase chars |
| metrics | JSON | Yes | Comparison data | Object with metrics |
| summary | Text | Yes | AI generated summary | Max 5000 chars |
| created_at | Timestamp | Yes | Comparison time | ISO 8601 |

### Entity: Export

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | UUID | Yes | Unique export identifier | Primary key |
| user_id | UUID | Yes | User who exported | Foreign key to User |
| source_type | Enum | Yes | What was exported | 'document', 'comparison' |
| source_id | UUID | Yes | Related entity ID | UUID |
| format | Enum | Yes | Export format | 'pdf', 'docx' |
| storage_path | String | Yes | File location | Unique |
| created_at | Timestamp | Yes | Export time | ISO 8601 |
| expires_at | Timestamp | Yes | When to delete | ISO 8601 |

### Relationships

- User has many Documents (one-to-many)
- User has many QueryHistory entries (one-to-many)
- User has many StockQueries (one-to-many)
- User has many StockComparisons (one-to-many)
- User has many Exports (one-to-many)
- Document has many QueryHistory entries (one-to-many)
- Document has many Exports (one-to-many)
- StockComparison has many Exports (one-to-many)

## Security Considerations

### Authentication & Authorization

- **Authentication Method**: JWT (JSON Web Tokens) with 24-hour expiration
- **Password Policy**: Minimum 8 characters, bcrypt hashing with cost factor 12
- **Token Storage**: Client stores JWT in httpOnly cookie (not localStorage to prevent XSS)
- **Session Management**: Redis-backed session store with sliding expiration
- **Authorization**: Role-based access control (RBAC) with user/admin roles
- **API Protection**: All endpoints except /auth/* require valid JWT in Authorization header

### Data Protection

- **Encryption at Rest**: 
  - Documents and exports encrypted using AES-256 before storage in blob service
  - Database encryption enabled at infrastructure level (PostgreSQL TDE)
  - Encryption keys managed via environment variables or key management service
  
- **Encryption in Transit**: 
  - HTTPS enforced for all connections (TLS 1.2 minimum, prefer TLS 1.3)
  - API responses use HTTPS with HSTS header
  - Internal service communication over encrypted channels

- **PII Handling**: 
  - Email addresses hashed for analytics and logging
  - User queries and documents never sent to third parties without explicit consent
  - Data retention policy: documents deleted after 90 days of inactivity (configurable)
  - GDPR compliance: users can request data export and account deletion

### Threat Model

| Threat | Mitigation | Priority |
|--------|------------|----------|
| SQL Injection | Use parameterized queries and ORM (SQLAlchemy) exclusively | High |
| XSS (Cross-Site Scripting) | Sanitize all user inputs, use Content Security Policy headers | High |
| CSRF (Cross-Site Request Forgery) | CSRF tokens for all state-changing operations | High |
| Unauthorized document access | Verify user_id matches document owner before any operation | High |
| DDoS attacks | Rate limiting: 100 req/min per user, 1000 req/min per IP | Medium |
| API key exposure | Never log sensitive data, use environment variables for secrets | High |
| Session hijacking | Short JWT expiration, refresh token rotation, IP validation | Medium |
| Malicious PDF uploads | File type validation, virus scanning, size limits | High |
| News scraping blocked | Respect robots.txt, implement exponential backoff, rotate user agents | Low |
| Data exfiltration via export | Audit logging of all exports, rate limit exports per user | Medium |


## Implementation Plan

### Phase 1: Foundation & Authentication (Duration: 1 week)

- [ ] Set up FastAPI project structure with virtual environment
- [ ] Configure PostgreSQL database and initial schema
- [ ] Implement user registration and login endpoints
- [ ] Create JWT authentication middleware
- [ ] Build basic HTML/CSS/JS frontend shell
- [ ] Implement responsive navigation and routing
- [ ] Set up development environment with hot reload
- [ ] Configure CORS and security headers

### Phase 2: Document Intelligence (Duration: 2 weeks)

- [ ] Implement PDF upload endpoint with validation
- [ ] Integrate Poppler for OCR and text extraction
- [ ] Set up ChromaDB for vector storage
- [ ] Implement text chunking and embedding pipeline
- [ ] Create RAG agent with LangChain/LlamaIndex
- [ ] Build document Q&A endpoint
- [ ] Create frontend upload interface with drag-and-drop
- [ ] Build chat interface for Q&A
- [ ] Implement document status polling
- [ ] Add citation display in answers

### Phase 3: Export & Sharing (Duration: 1 week)

- [ ] Implement PDF export service with WeasyPrint/ReportLab
- [ ] Implement DOCX export with python-docx
- [ ] Set up Gmail SMTP service with app password
- [ ] Create export endpoints (PDF, DOCX, Email)
- [ ] Build export UI with format selection
- [ ] Implement email modal with recipient input
- [ ] Add export download management
- [ ] Configure temporary file cleanup

### Phase 4: News Feed (Duration: 1.5 weeks)

- [ ] Implement RSS feed parser for CNBC, BBC, TechCrunch
- [ ] Set up background scheduler (APScheduler/Celery)
- [ ] Create news storage and caching layer (Redis)
- [ ] Implement AI summarization endpoint
- [ ] Build news feed API endpoint with pagination
- [ ] Create scrolling news feed UI
- [ ] Implement click-to-summarize functionality
- [ ] Add source filtering and sorting
- [ ] Configure RSS feed polling frequency

### Phase 5: Stock Ticker Agent (Duration: 1.5 weeks)

- [ ] Integrate yfinance library
- [ ] Implement ticker validation and data fetching
- [ ] Create stock RAG agent for natural language queries
- [ ] Build stock query endpoint with context retention
- [ ] Create stock query UI with ticker input
- [ ] Implement conversational chat interface
- [ ] Add query history display
- [ ] Handle invalid ticker errors gracefully

### Phase 6: Stock Comparison (Duration: 1 week)

- [ ] Implement stock comparison logic
- [ ] Create comparison calculation service
- [ ] Build AI summary generation for comparisons
- [ ] Implement comparison endpoint
- [ ] Create comparison UI with dual ticker input
- [ ] Build side-by-side metric display table
- [ ] Add comparison summary section
- [ ] Integrate export functionality for comparisons

### Phase 7: Polish & Testing (Duration: 1 week)

- [ ] Write comprehensive unit tests
- [ ] Implement integration tests for all flows
- [ ] Create E2E tests for user journeys
- [ ] Perform security audit and penetration testing
- [ ] Conduct performance testing and optimization
- [ ] Fix identified bugs and issues
- [ ] Improve error messages and user feedback
- [ ] Optimize responsive design for mobile
- [ ] Add loading states and progress indicators
- [ ] Write user documentation

### Dependencies

- **External APIs**: 
  - Groq API key for LLM (required before Phase 2)
  - Gmail SMTP credentials with app password (required before Phase 3)
  - RSS feed URLs for CNBC, BBC, TechCrunch (publicly available, required before Phase 4)
  
- **Infrastructure**: 
  - PostgreSQL database instance (required before Phase 1)
  - Redis instance (required before Phase 4)
  - Local storage directory with write permissions (required before Phase 2)
  - ChromaDB setup (required before Phase 2)

- **Internal Dependencies**:
  - Phase 2 depends on Phase 1 (authentication)
  - Phase 3 depends on Phase 2 (document analysis to export)
  - Phase 5 and 6 are independent of Phases 2-4
  - Phase 7 depends on all previous phases

## Monitoring & Observability

### Metrics to Track

- **Document Processing**: 
  - Upload success rate (target: > 99%)
  - Average processing time (target: < 30 seconds)
  - OCR accuracy rate (target: > 95%)
  - Failed processing reasons (categorized)

- **Q&A Performance**:
  - Query response time p50, p95, p99 (target: p95 < 3s)
  - RAG retrieval accuracy (manual sampling)
  - Queries per document (average)
  - Failed queries (error categorization)

- **News Feed**:
  - RSS feed fetch success rate per source (target: > 95%)
  - Articles fetched per cycle (count)
  - Summarization request rate
  - Summary generation time (target: < 2s)

- **Stock Queries**:
  - yfinance API success rate (target: > 99%)
  - Query response time (target: < 1s)
  - Invalid ticker rate (tracking)
  - Queries per user per day (average)

- **System Health**:
  - API endpoint response times (all endpoints)
  - Error rates by endpoint (target: < 1%)
  - Database query performance
  - Cache hit rates (Redis)
  - Active user sessions (concurrent count)

### Alerts

- **Critical Alerts** (immediate notification):
  - API error rate > 5% for 5 minutes → Page on-call engineer
  - Database connection failures → Page on-call engineer
  - Document processing failures > 20% for 10 minutes → Alert team
  - Authentication service down → Page on-call engineer

- **Warning Alerts** (notification within 30 min):
  - RSS feed fetch failing for any source > 3 consecutive cycles → Alert team
  - yfinance API rate limiting detected → Alert team
  - Local storage usage > 80% capacity → Alert team
  - Response time p95 > 5 seconds for 15 minutes → Alert team

- **Info Alerts** (daily digest):
  - Total documents processed (count)
  - New user registrations (count)
  - Most queried tickers (top 10)
  - Most popular news sources (breakdown)

### Logging

- **Events to Log**:
  - All API requests (method, endpoint, status, duration, user_id)
  - Authentication events (login, logout, failed attempts)
  - Document operations (upload, processing start/end, queries)
  - Export operations (format, document, user)
  - RSS feed fetch cycles (source, articles found, errors)
  - Stock queries (ticker, question length, response time)
  - Error stack traces (with sanitized user data)
  - Security events (rate limiting triggered, suspicious activity)

- **Log Levels**:
  - ERROR: Application errors, failed operations, exceptions
  - WARN: Degraded performance, retries, non-critical issues
  - INFO: Successful operations, business events
  - DEBUG: Detailed flow information (development only)

- **Log Retention**:
  - ERROR/WARN logs: 90 days
  - INFO logs: 30 days
  - DEBUG logs: 7 days
  - Structured logging format (JSON) for easy parsing
  - Centralized logging (CloudWatch/ELK/Datadog)

## Rollout & Rollback

### Deployment Strategy

- **Initial Deployment**: Blue-green deployment to minimize downtime
  - Green environment: New version with all features
  - Blue environment: Kept running during validation
  - Traffic cutover after smoke tests pass
  - Blue environment kept as instant rollback target for 24 hours

- **Feature Flags**:
  - News feed feature (can disable if scraping issues)
  - Stock comparison feature (can disable if yfinance issues)
  - Export email feature (can disable if SMTP issues)
  - AI summarization (can fall back to excerpts)
  - Document upload (can disable if processing overloaded)

- **Deployment Stages**:
  1. Deploy to staging environment
  2. Run automated test suite
  3. Perform manual smoke testing
  4. Deploy to production green environment
  5. Run production smoke tests (health checks)
  6. Gradually shift traffic (10%, 50%, 100%)
  7. Monitor metrics for 1 hour
  8. Decommission blue environment if stable

### Rollback Plan

1. **Rollback Trigger Conditions**:
   - Error rate > 10% for any endpoint
   - Critical feature completely non-functional
   - Data corruption detected
   - Security vulnerability discovered in new version

2. **Rollback Steps**:
   - Immediately switch traffic back to blue environment
   - Verify blue environment health and metrics
   - Investigate root cause in green environment
   - Determine if hotfix possible or full revert needed
   - Communicate incident to users if impacted

3. **Data Migration Considerations**:
   - All schema migrations must be backward compatible for 1 version
   - No destructive migrations in initial rollout
   - Database changes deployed separately before application deployment
   - Rollback scripts prepared and tested for all migrations

## Success Criteria

The Finalytics MVP Platform will be considered successfully delivered when the following measurable outcomes are achieved:

### User Capability Criteria

- [ ] Users can upload a 100-page financial document and begin asking questions within 30 seconds
- [ ] Users receive accurate answers to natural language questions about uploaded documents in under 3 seconds per query
- [ ] Users can export their analysis session as a formatted PDF or DOCX with preserved content and citations
- [ ] Users can send analysis reports via email directly from the platform
- [ ] Users see breaking financial news appear in their feed within 5 minutes of publication
- [ ] Users can click any news headline and receive an AI-generated summary within 2 seconds
- [ ] Users can enter a stock ticker and ask natural language questions receiving real-time data in under 1 second
- [ ] Users can compare two stocks side-by-side and view an AI-generated summary of differences
- [ ] Users can access the platform on mobile devices with full functionality and responsive layout

### System Performance Criteria

- [ ] Document processing completes in under 30 seconds for 95% of uploads (up to 100 pages)
- [ ] Q&A response time averages under 3 seconds at 95th percentile
- [ ] News feed loads and displays 50 articles in under 1 second
- [ ] News summarization completes in under 2 seconds per article
- [ ] Stock queries return results in under 1 second at 95th percentile
- [ ] Stock comparisons generate full analysis in under 2 seconds
- [ ] Platform supports 100 concurrent users without performance degradation
- [ ] API error rate remains below 1% under normal operating conditions

### Quality & Accuracy Criteria

- [ ] OCR achieves greater than 95% accuracy on standard financial documents (verified through sampling)
- [ ] RAG Q&A provides relevant answers with appropriate citations for 90% of queries (measured through user feedback)
- [ ] News summaries accurately capture key points without introducing errors (verified through manual review sampling)
- [ ] Stock data accuracy matches Yahoo Finance source data (100% accuracy on available data points)
- [ ] Export documents preserve all formatting, content, and citations without data loss

### Security & Compliance Criteria

- [ ] All user authentication uses secure JWT tokens with appropriate expiration
- [ ] All user documents are encrypted at rest using AES-256
- [ ] All API connections enforce HTTPS with TLS 1.2+
- [ ] Users can only access their own documents and data (verified through security testing)
- [ ] Platform meets WCAG 2.1 AA accessibility standards (verified through automated and manual testing)
- [ ] Rate limiting prevents abuse (100 requests per minute per user)
- [ ] Password policies enforce minimum security standards (8+ characters, bcrypt hashing)

### User Experience Criteria

- [ ] New users can register, log in, and upload their first document within 2 minutes
- [ ] Users report satisfaction with interface clarity and ease of use (survey score > 4.0/5.0)
- [ ] Error messages are clear and actionable when failures occur
- [ ] Platform works on screens as small as 320px width (mobile responsive)
- [ ] All primary workflows (upload, query, export, compare) have success rates > 95%

### Operational Readiness Criteria

- [ ] Automated test suite achieves > 80% code coverage
- [ ] All critical user journeys have end-to-end tests
- [ ] Monitoring and alerting configured for all key metrics
- [ ] Runbook documentation complete for common operational tasks
- [ ] Backup and disaster recovery procedures tested and documented
- [ ] Performance benchmarks established and documented
- [ ] Security audit completed with no high-severity findings

## Assumptions

This specification makes the following assumptions:

1. **External Services**:
   - Groq API has sufficient rate limits for expected load (fast inference speeds)
   - yfinance library will continue providing free access to Yahoo Finance data
   - RSS feeds from CNBC, BBC, TechCrunch will remain publicly available and stable
   - Gmail SMTP will be reliable for export sharing (500 emails/day limit sufficient for MVP)

2. **User Behavior**:
   - Average document size will be 5-20MB (10-K filings typically 50-200 pages)
   - Users will ask 3-10 questions per document on average
   - Peak concurrent users will not exceed 100 in MVP phase
   - Users primarily access from desktop browsers (mobile is secondary)

3. **Data & Content**:
   - Financial documents will be primarily in English
   - Document quality will be sufficient for OCR (not severely degraded scans)
   - RSS feed formats will remain stable (standard RSS 2.0/Atom format)
   - Stock tickers will follow standard format (1-5 uppercase letters)

4. **Technical Environment**:
   - PostgreSQL database will have sufficient storage for 10,000 users and documents
   - Local filesystem will have sufficient capacity for document and export storage (MVP only; production will migrate to cloud storage)
   - Redis cache will have adequate memory for news feed and session caching
   - Server has adequate disk space for file storage (minimum 100GB recommended)

5. **Timeline & Resources**:
   - 8-week implementation timeline is based on 2-3 full-time developers
   - External API costs (Groq LLM, infrastructure) fit within allocated budget
   - No major scope changes will be requested during MVP development
   - Testing and QA resources will be available in final phase

6. **Compliance & Legal**:
   - Using RSS feeds for news aggregation is legally permissible (feeds are publicly syndicated)
   - Using yfinance for non-commercial platform is acceptable per terms of service
   - GDPR compliance requirements are satisfied by basic data protection measures
   - No specific financial regulations (SEC, FINRA) apply to this platform

## Clarifications

### Session 2025-10-28

- Q: Which LLM provider should be used for RAG Q&A, summarization, and comparison generation? → A: Groq
- Q: Which vector store should be used for document embeddings and retrieval? → A: ChromaDB
- Q: Which email service provider should be used for sending analysis reports? → A: Gmail SMTP
- Q: Which blob storage provider should be used for documents and exports? → A: Local filesystem (MVP/dev; migrate to S3/Azure for production)
- Q: Which approach should be used for news scraping? → A: RSS/Atom feeds (free, reliable, officially supported)

## Open Questions

This section intentionally left empty - all critical decisions have been made with reasonable defaults. No clarifications needed to proceed with implementation.

## Appendix

### References

- **Constitutional Principles**: `.specify/memory/constitution.md`
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **yfinance Library**: https://github.com/ranaroussi/yfinance
- **LangChain Documentation**: https://python.langchain.com/docs/
- **Poppler PDF Tools**: https://poppler.freedesktop.org/
- **WCAG 2.1 AA Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

### Technology Stack Summary

**Backend**:
- FastAPI (Python 3.9+)
- SQLAlchemy ORM + Alembic migrations
- PostgreSQL database
- Redis cache
- LangChain/LlamaIndex for RAG
- ChromaDB for vector storage
- Groq for LLM inference
- yfinance for stock data
- Poppler/PyPDF for PDF processing
- feedparser for RSS feed parsing
- WeasyPrint/ReportLab for PDF export
- python-docx for DOCX export
- smtplib for email

**Frontend**:
- Vanilla HTML5
- CSS3 with Flexbox/Grid
- Vanilla JavaScript (ES6+)
- Fetch API for REST calls
- No framework dependencies

**Infrastructure**:
- Docker containers
- PostgreSQL 14+
- Redis 7+
- Local filesystem storage (MVP; migrate to S3/Azure for production)
- ChromaDB for vectors

### Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-28 | Finalytics Team | Initial draft - Complete MVP specification |

---

**Specification Status**: This document is ready for planning and implementation. All constitutional principle alignments have been validated. Proceed to `/speckit.plan` to create detailed implementation tasks.

