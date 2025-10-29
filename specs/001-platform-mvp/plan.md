# Project Plan: Finalytics MVP Platform

## Overview

**Feature**: Complete Finalytics MVP Platform implementing all 5 constitutional principles  
**Priority**: High  
**Estimated Effort**: Large (8 weeks, 2-3 developers)  
**Target Release**: v1.0.0-MVP

## Constitution Alignment
 
### Principle Compliance Check

- [x] **Principle 1 (On-Demand Document Intelligence)**: ✅ Core feature - 10-K Analyzer with PDF upload, OCR, RAG Q&A
- [x] **Principle 2 (Actionable & Shareable Analysis)**: ✅ Core feature - PDF/DOCX export, email sharing
- [x] **Principle 3 (Real-Time Market Awareness)**: ✅ Core feature - RSS news feed with AI summarization
- [x] **Principle 4 (Live Ticker RAG Agent)**: ✅ Core feature - Yahoo Finance integration with natural language queries
- [x] **Principle 5 (Seamless Comparative Analysis)**: ✅ Core feature - Stock comparison tool with side-by-side metrics

**Impact Summary**: This plan implements ALL five constitutional principles from the ground up. The MVP delivers a complete financial analytics platform with intelligent document processing (P1), collaborative export/sharing (P2), real-time news awareness (P3), conversational stock data access (P4), and comparative analysis capabilities (P5). Every implementation phase directly maps to constitutional requirements, ensuring full compliance with the project's governance framework.

## Objectives

1. **Primary**: Deliver a fully functional MVP implementing all 5 constitutional principles within 8 weeks
2. **Secondary**: Establish a simple, maintainable tech stack (FastAPI + vanilla JS) that enables rapid iteration
3. **Tertiary**: Create comprehensive developer documentation and quickstart guides for smooth onboarding

## Success Criteria

- [ ] Users can upload 100-page PDFs and query them within 30 seconds (Principle 1)
- [ ] Users can export analyses as PDF/DOCX and email them (Principle 2)
- [ ] News feed updates every 5 minutes with on-demand AI summaries (Principle 3)
- [ ] Stock queries return real-time data in under 1 second (Principle 4)
- [ ] Stock comparisons generate complete analysis within 2 seconds (Principle 5)
- [ ] Platform supports 100 concurrent users without degradation
- [ ] All endpoints have <1% error rate under normal load
- [ ] Mobile-responsive interface works on 320px+ screens
- [ ] User authentication secures all features with JWT tokens
- [ ] Developer can set up local environment in under 30 minutes

## Technical Approach

### Architecture

**Three-Tier Architecture**:

```
┌─────────────────────────────────────┐
│   Presentation Layer (Frontend)    │
│   - Vanilla HTML/CSS/JS             │
│   - Responsive design               │
│   - REST API consumers              │
└──────────────┬──────────────────────┘
               │ HTTPS/REST
┌──────────────▼──────────────────────┐
│   Application Layer (FastAPI)      │
│   - Business logic services         │
│   - RAG agents (Groq + ChromaDB)    │
│   - Authentication (JWT)            │
│   - API routes & validation         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Data Layer                        │
│   - PostgreSQL (structured data)    │
│   - ChromaDB (vector embeddings)    │
│   - Redis (caching & sessions)      │
│   - Local FS (document storage)     │
└─────────────────────────────────────┘
```

**Key Architectural Decisions**:
1. **Monolithic MVP**: Single FastAPI application for simplicity; can extract microservices later
2. **Stateless API**: JWT authentication enables horizontal scaling
3. **Background Jobs**: APScheduler for news scraping (can migrate to Celery if needed)
4. **Vector Isolation**: ChromaDB collections per document prevent cross-contamination

### Key Components

1. **Document Intelligence Service** (Principle 1)
   - PDF upload handler with multipart form support
   - OCR pipeline using Poppler (pdf2image + pytesseract)
   - Text chunking strategy (512 tokens with 50 token overlap)
   - ChromaDB vector storage per document namespace
   - RAG agent using LangChain with Groq LLM
   - Citation extraction from chunk metadata

2. **Export & Sharing Service** (Principle 2)
   - PDF generation using WeasyPrint (HTML → PDF)
   - DOCX generation using python-docx
   - Email delivery via Gmail SMTP
   - Template rendering for formatted exports
   - Temporary file management with expiration

3. **News Feed Service** (Principle 3)
   - RSS feed parser using feedparser library
   - Background scheduler (APScheduler) for 5-minute polling
   - Redis caching for news articles
   - Article summarization using Groq
   - Source-specific feed URL configuration

4. **Stock Data Service** (Principle 4)
   - yfinance integration for market data
   - RAG agent for natural language processing
   - Session-based context retention
   - Ticker validation and error handling
   - Real-time data caching strategy

5. **Stock Comparison Service** (Principle 5)
   - Parallel data fetching for two tickers
   - Metric calculation and normalization
   - Comparison summary generation via Groq
   - Export integration with Service #2

6. **Authentication Service** (All Principles)
   - User registration with password hashing (bcrypt)
   - JWT token generation and validation
   - Session management via Redis
   - Password policy enforcement
   - CORS and security headers

### Technology Stack

- **Language/Framework**: Python 3.9+ with FastAPI
- **Libraries**:
  - **Core**: FastAPI, Uvicorn, Pydantic, SQLAlchemy
  - **AI/ML**: LangChain, ChromaDB, Groq SDK
  - **Document Processing**: Poppler, pdf2image, pytesseract, PyPDF2
  - **Export**: WeasyPrint, python-docx
  - **Data**: psycopg2, redis-py, feedparser, yfinance
  - **Auth**: python-jose (JWT), passlib (bcrypt)
  - **Scheduling**: APScheduler
  - **Testing**: pytest, pytest-asyncio, httpx
- **External APIs**: 
  - Groq API for LLM inference
  - Gmail SMTP for email delivery
  - RSS feeds (CNBC, BBC, TechCrunch)
  - Yahoo Finance via yfinance

## Implementation Phases

### Phase 1: Foundation & Authentication (Duration: 1 week)

**Deliverables**:
- [ ] FastAPI project structure with environment setup
- [ ] PostgreSQL database with Alembic migrations
- [ ] User registration and login endpoints
- [ ] JWT authentication middleware
- [ ] Basic HTML/CSS/JS frontend shell
- [ ] Responsive navigation and routing
- [ ] CORS and security headers configured
- [ ] Health check and status endpoints

**Key Tasks**:
1. Initialize FastAPI project with poetry/pip
2. Configure PostgreSQL connection and create User table
3. Implement password hashing with bcrypt (cost factor 12)
4. Create JWT token generation (HS256, 24h expiration)
5. Build authentication middleware for protected routes
6. Create frontend file structure (static/, templates/)
7. Implement login/signup forms with client-side validation
8. Set up CORS for local development

**Success Criteria**: User can register, login, and access protected dashboard

### Phase 2: Document Intelligence (Duration: 2 weeks)

**Deliverables**:
- [ ] PDF upload endpoint with validation (50MB max)
- [ ] OCR pipeline integrated (Poppler + pytesseract)
- [ ] ChromaDB vector storage configured
- [ ] Text chunking and embedding pipeline
- [ ] RAG agent with document-scoped retrieval
- [ ] Document Q&A endpoint with citations
- [ ] Frontend upload UI with drag-and-drop
- [ ] Real-time chat interface for Q&A
- [ ] Document status polling mechanism
- [ ] Citation display in answer bubbles

**Key Tasks**:
1. Create Document model with status enum (uploading/processing/ready/error)
2. Implement multipart form handler for PDF uploads
3. Integrate Poppler for OCR (handle both text and scanned PDFs)
4. Design chunking strategy (512 tokens, 50 overlap, preserve paragraphs)
5. Set up ChromaDB with document-specific collections
6. Generate embeddings using Groq embedding model
7. Build RAG agent with LangChain (retrieval → context → generation)
8. Extract page numbers from chunk metadata for citations
9. Create WebSocket or polling endpoint for upload progress
10. Build frontend chat UI with message history

**Success Criteria**: User uploads 10-K PDF, asks "What was Q4 revenue?", gets answer with page citations in <30 seconds

### Phase 3: Export & Sharing (Duration: 1 week)

**Deliverables**:
- [ ] PDF export service with WeasyPrint
- [ ] DOCX export service with python-docx
- [ ] Gmail SMTP email integration
- [ ] Export endpoints (PDF, DOCX, Email)
- [ ] Frontend export UI with format selection
- [ ] Email modal with recipient input and preview
- [ ] Export download management
- [ ] Temporary file cleanup scheduler

**Key Tasks**:
1. Create Export model to track exports and expiration
2. Build HTML template for formatted analysis reports
3. Integrate WeasyPrint for PDF generation (CSS styling for professional output)
4. Implement python-docx for DOCX generation (preserve structure)
5. Configure Gmail SMTP with app password (handle authentication)
6. Create email composition with attachment or inline HTML
7. Build frontend export buttons with format dropdown
8. Implement email modal with form validation
9. Set up background task to delete expired exports (24h TTL)
10. Add export history to user dashboard

**Success Criteria**: User exports analysis as PDF, opens in viewer with proper formatting; emails to recipient successfully

### Phase 4: News Feed (Duration: 1.5 weeks)

**Deliverables**:
- [ ] RSS feed parser for CNBC, BBC, TechCrunch
- [ ] APScheduler background job (5-minute interval)
- [ ] NewsArticle model and storage layer
- [ ] Redis caching for news feed
- [ ] AI summarization endpoint
- [ ] News feed API with pagination
- [ ] Frontend scrolling news feed UI
- [ ] Click-to-summarize interaction
- [ ] Source filtering and sorting
- [ ] RSS feed health monitoring

**Key Tasks**:
1. Create NewsArticle model with source enum
2. Configure feedparser with RSS feed URLs
3. Implement feed fetching logic with error handling
4. Set up APScheduler to run scraper every 5 minutes
5. Store articles in PostgreSQL, cache in Redis (1 hour TTL)
6. Build summarization prompt for Groq (3-5 sentence format)
7. Create /api/news/feed endpoint with filtering
8. Implement on-demand summarization with caching
9. Build frontend feed with infinite scroll
10. Add click handlers for expanding summaries

**Success Criteria**: News feed shows latest articles within 5 minutes of publication; clicking headline shows AI summary in <2 seconds

### Phase 5: Stock Ticker Agent (Duration: 1.5 weeks)

**Deliverables**:
- [ ] yfinance integration with error handling
- [ ] Ticker validation logic
- [ ] Stock RAG agent for natural language queries
- [ ] Stock query endpoint with context retention
- [ ] StockQuery model for history
- [ ] Frontend stock query UI with ticker input
- [ ] Conversational chat interface
- [ ] Query history display
- [ ] Invalid ticker error messaging

**Key Tasks**:
1. Create StockQuery model to store queries and responses
2. Integrate yfinance for fetching stock data (price, metrics, history)
3. Implement ticker validation (format check + yfinance lookup)
4. Build RAG agent with stock data context formatting
5. Design prompts for conversational financial queries
6. Create session-based context retention (Redis)
7. Implement /api/stocks/query endpoint
8. Build frontend ticker input with autocomplete
9. Create chat interface similar to document Q&A
10. Add query history sidebar with timestamps

**Success Criteria**: User enters "AAPL", asks "What's the current price and 52-week high?", gets real-time answer in <1 second

### Phase 6: Stock Comparison (Duration: 1 week)

**Deliverables**:
- [ ] Stock comparison logic with parallel fetching
- [ ] Comparison calculation service
- [ ] AI summary generation for comparisons
- [ ] Comparison endpoint
- [ ] StockComparison model for history
- [ ] Frontend comparison UI with dual ticker input
- [ ] Side-by-side metric display table
- [ ] Comparison summary section
- [ ] Export integration for comparisons

**Key Tasks**:
1. Create StockComparison model to store comparison results
2. Implement parallel yfinance fetching for two tickers
3. Extract and normalize key metrics (price, market cap, P/E, volume, etc.)
4. Calculate percentage differences and relative performance
5. Build comparison summary prompt for Groq
6. Create /api/stocks/compare endpoint
7. Build frontend form with two ticker inputs
8. Design comparison table with highlighting for differences
9. Display AI-generated summary below table
10. Add "Export Comparison" button (integrates with Phase 3)

**Success Criteria**: User compares MSFT vs GOOGL, sees side-by-side metrics and AI summary within 2 seconds

### Phase 7: Polish & Documentation (Duration: 1 week)

**Deliverables**:
- [ ] Comprehensive API documentation (OpenAPI/Swagger)
- [ ] User guide with screenshots
- [ ] Developer quickstart guide
- [ ] Deployment runbook
- [ ] Error message improvements
- [ ] Loading states and progress indicators
- [ ] Mobile responsive optimizations
- [ ] Performance profiling and optimization
- [ ] Security audit and fixes
- [ ] Bug fixes and edge case handling

**Key Tasks**:
1. Generate OpenAPI schema from FastAPI
2. Write user guide covering all 5 principles
3. Create developer quickstart (see quickstart.md)
4. Document deployment procedure (Docker + docker-compose)
5. Improve error messages with actionable guidance
6. Add loading spinners and skeleton screens
7. Test responsive design on multiple devices
8. Profile slow endpoints and optimize queries
9. Run security scan (bandit, safety)
10. Fix identified bugs from user testing

**Success Criteria**: New developer can set up local environment in <30 minutes using quickstart guide; all features work smoothly on mobile

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Groq API rate limits exceeded | Medium | High | Implement request queue with backoff; cache responses aggressively; monitor usage daily |
| OCR accuracy below 95% on scanned docs | Medium | High | Test with diverse document samples early; use multiple OCR engines (Tesseract + EasyOCR); allow manual text corrections |
| RSS feeds change format or become unavailable | Low | Medium | Monitor feed health daily; implement fallback to direct article scraping; support multiple feeds per source |
| yfinance library breaking changes | Low | Medium | Pin library version; create wrapper abstraction layer; monitor library releases |
| ChromaDB vector search performance degrades with many documents | Medium | Medium | Implement collection per document strategy; limit max documents per user; profile query performance |
| Gmail SMTP blocks automated emails | Low | High | Use app-specific password; implement email verification; add daily sending limits; have backup SMTP provider ready |
| Local filesystem storage fills up | High | Medium | Implement automatic cleanup of old documents (90 days); monitor disk usage; alert at 80% capacity |
| Background scheduler failures | Medium | Medium | Add health checks for scheduler; implement retry logic; log all job failures; alert on consecutive failures |
| JWT token security vulnerabilities | Low | Critical | Use strong secret key (256-bit); implement token rotation; short expiration (24h); blacklist on logout |
| Concurrent user scaling issues | Medium | High | Load test early with 100+ concurrent users; implement connection pooling; use Redis for session sharing |

## Dependencies

- **Internal**: None (greenfield project)
- **External**:
  - Groq API key (required Phase 2+) - Sign up at groq.com
  - Gmail account with app password (required Phase 3) - Configure in Google account settings
  - PostgreSQL 14+ instance (required Phase 1)
  - Redis 7+ instance (required Phase 4)
  - Domain name for production deployment (optional for MVP)
- **Timeline Critical Path**:
  - Phase 2 blocks Phase 3 (need document analysis before export)
  - Phase 4, 5, 6 can run in parallel after Phase 1
  - Phase 7 blocks production release

## Rollout Plan

1. **Development** (Weeks 1-7)
   - Phases 1-6 executed sequentially
   - Daily standups to track progress
   - Weekly demos to stakeholders
   - Continuous integration with automated tests

2. **Final Testing & Polish** (Week 8)
   - Phase 7 execution
   - User acceptance testing with 5-10 beta testers
   - Performance testing with load simulation
   - Security audit and fixes
   - Bug bash sessions

3. **Staging Deployment** (Week 8, Day 5)
   - Deploy to staging environment
   - Smoke tests on all 5 principles
   - Invite internal team for final validation
   - Monitor logs and metrics for 24 hours

4. **Production Deployment** (Week 8, Day 7)
   - Blue-green deployment strategy
   - Gradual traffic shift (10% → 50% → 100%)
   - Monitor error rates and response times
   - Keep rollback plan ready for 24 hours

5. **Monitoring** (Post-Launch)
   - Track key metrics:
     - User registrations per day
     - Documents uploaded per day
     - Average document processing time
     - News feed update frequency
     - Stock queries per day
     - API error rates by endpoint
     - Concurrent user count peaks
   - Alert on:
     - Error rate > 5%
     - Processing time > 45 seconds
     - RSS feed failures > 3 consecutive
     - Groq API errors
     - Disk usage > 80%

## Documentation Requirements

- [x] API documentation - OpenAPI/Swagger auto-generated from FastAPI
- [x] User guide - Step-by-step walkthrough of all features with screenshots
- [x] Developer quickstart - See quickstart.md in specs directory
- [x] Architecture Decision Records (ADRs) - Document key technical choices
- [x] Runbook for operations - Deployment, monitoring, troubleshooting procedures
- [x] Data model documentation - See data-model.md in specs directory
- [x] API contract specifications - See contracts/ directory for endpoint specs

---

**Plan Version**: 1.0  
**Created**: 2025-10-28  
**Last Updated**: 2025-10-28  
**Owner**: Finalytics Engineering Team

**Next Steps**:
1. Review and approve this plan
2. Set up development environment using quickstart.md
3. Begin Phase 1: Foundation & Authentication
4. Schedule weekly checkpoint meetings
5. Track progress in project management tool

