# Technical Research & Decisions: Finalytics MVP

## Document Control

**Created**: 2025-10-28  
**Purpose**: Document all technical decisions, research findings, and rationale for technology choices  
**Status**: Final


---

## Executive Summary

This document captures the research and decision-making process for the Finalytics MVP Platform. All technology choices prioritize simplicity, cost-effectiveness, and rapid MVP development while maintaining clear upgrade paths for production scaling.

---

## Decision 1: LLM Provider

### Decision
**Use Groq for all LLM inference** (RAG Q&A, summarization, stock analysis)

### Rationale
- **Speed**: Groq offers fastest inference speeds (up to 10x faster than alternatives)
- **Cost**: Competitive pricing with generous free tier for MVP development
- **Quality**: Supports leading models (Llama, Mixtral) with strong performance
- **API Simplicity**: OpenAI-compatible API makes integration straightforward
- **Developer Experience**: Well-documented Python SDK

### Alternatives Considered
- **OpenAI GPT-4**: Higher cost, slower inference, but better for complex reasoning
- **Anthropic Claude**: Longer context windows, but higher cost and slower
- **Local LLMs**: No API costs, but requires GPU infrastructure and ops overhead

### Implementation Notes
```python
# Groq SDK usage pattern
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])
completion = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[{"role": "user", "content": query}],
    temperature=0.7,
    max_tokens=1024
)
```

### Risks & Mitigations
- **Risk**: Rate limiting in production
- **Mitigation**: Implement request queue with exponential backoff; cache responses aggressively

---

## Decision 2: Vector Database

### Decision
**Use ChromaDB for vector storage and retrieval**

### Rationale
- **Embedded Mode**: Runs in-process with no separate server (simpler deployment)
- **Persistence**: Built-in disk persistence without external database
- **Python Native**: First-class Python support with clean API
- **Collections**: Document isolation via named collections
- **Performance**: Fast enough for MVP with <10K documents per user
- **Migration Path**: Can scale to client-server mode later if needed

### Alternatives Considered
- **FAISS**: Faster at scale, but requires manual persistence layer
- **Pinecone**: Managed service, but adds cost and external dependency
- **Weaviate**: Powerful features, but overkill for MVP and adds complexity
- **Qdrant**: Good alternative, but less Python-focused than Chroma

### Implementation Notes
```python
# ChromaDB setup
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_data"
))

# Document-scoped collection
collection = client.get_or_create_collection(
    name=f"doc_{document_id}",
    metadata={"document_id": document_id}
)
```

### Performance Targets
- Query latency: <100ms for similarity search
- Indexing speed: <5 seconds for 100-page document
- Storage: ~1MB per 100 pages of embedded text

---

## Decision 3: Email Service

### Decision
**Use Gmail SMTP for email delivery**

### Rationale
- **Zero Cost**: Free for up to 500 emails/day (sufficient for MVP)
- **Simple Setup**: Just need Gmail account + app password
- **Reliability**: Google's infrastructure ensures high deliverability
- **No Verification**: Unlike AWS SES, no domain verification needed
- **Fast Integration**: Python `smtplib` built-in support

### Alternatives Considered
- **SendGrid**: Free tier (100 emails/day), better analytics, but adds external dependency
- **AWS SES**: Scalable and cheap, but requires domain verification
- **Mailgun**: Good developer experience, but costs money from day 1
- **Postmark**: Excellent deliverability, but no free tier

### Implementation Notes
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email(to: str, subject: str, body: str, attachment_path: str = None):
    msg = MIMEMultipart()
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
        server.send_message(msg)
```

### Risks & Mitigations
- **Risk**: Gmail blocks automated sending
- **Mitigation**: Use app-specific password; implement daily sending limits (100/day); verify recipient addresses

---

## Decision 4: Blob Storage

### Decision
**Use local filesystem for MVP** with clear migration path to S3/Azure for production

### Rationale
- **Zero Cost**: No cloud storage fees during development
- **Simplicity**: No API credentials or SDK integration needed
- **Fast Iteration**: Direct file access for debugging
- **Sufficient for MVP**: Expected <100GB total storage
- **Easy Migration**: Can swap to S3 with minimal code changes using abstraction layer

### Alternatives Considered
- **AWS S3**: Industry standard, very cheap, but adds deployment complexity
- **Azure Blob Storage**: Similar to S3, good if using Azure ecosystem
- **MinIO**: Self-hosted S3-compatible, but adds operational overhead

### Implementation Notes
```python
# Storage abstraction for easy migration
from abc import ABC, abstractmethod
from pathlib import Path

class StorageBackend(ABC):
    @abstractmethod
    def save(self, key: str, data: bytes) -> str: pass
    
    @abstractmethod
    def load(self, key: str) -> bytes: pass
    
    @abstractmethod
    def delete(self, key: str) -> None: pass

class LocalFileStorage(StorageBackend):
    def __init__(self, base_path: str = "./storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, data: bytes) -> str:
        file_path = self.base_path / key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        return str(file_path)
    
    def load(self, key: str) -> bytes:
        return (self.base_path / key).read_bytes()
    
    def delete(self, key: str) -> None:
        (self.base_path / key).unlink(missing_ok=True)

# Future S3 implementation
class S3Storage(StorageBackend):
    # Implementation using boto3
    pass
```

### Production Migration Plan
1. Implement `S3Storage` class using boto3
2. Update storage config to use S3 backend
3. Run one-time migration script to copy local files to S3
4. Deploy with new config
5. Verify all file operations work
6. Delete local files after 30-day safety period

---

## Decision 5: News Scraping Approach

### Decision
**Use RSS/Atom feeds** from financial news sources

### Rationale
- **Free & Legal**: RSS feeds are publicly available and intended for consumption
- **Structured Data**: XML format with consistent schema (title, link, date, description)
- **Reliable**: Feeds don't break with website redesigns (unlike HTML scraping)
- **No Rate Limiting**: Most RSS feeds have no rate limits for reasonable polling
- **Easy Parsing**: Python `feedparser` library handles all feed formats

### Alternatives Considered
- **Web Scraping HTML**: More flexible, but breaks with UI changes and may violate ToS
- **News APIs (NewsAPI, Aylien)**: Paid services with better aggregation, but adds cost
- **Twitter/X API**: Real-time, but requires API access and costs money

### Implementation Notes
```python
import feedparser
from datetime import datetime

RSS_FEEDS = {
    "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "bbc": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "techcrunch": "https://techcrunch.com/feed/"
}

def fetch_feed(source: str) -> list:
    feed_url = RSS_FEEDS[source]
    feed = feedparser.parse(feed_url)
    
    articles = []
    for entry in feed.entries[:50]:  # Limit to latest 50
        articles.append({
            "title": entry.title,
            "url": entry.link,
            "published_at": datetime(*entry.published_parsed[:6]),
            "description": entry.get("summary", "")
        })
    return articles
```

### Feed Monitoring Strategy
- Poll each feed every 5 minutes via APScheduler
- Track consecutive failures per source (alert after 3)
- Cache articles in Redis (1 hour TTL)
- Store articles in PostgreSQL for history

---

## Decision 6: Background Job Processing

### Decision
**Use APScheduler for background jobs** (news scraping, file cleanup)

### Rationale
- **Simplicity**: Runs in-process with FastAPI (no separate worker process)
- **Sufficient for MVP**: Handles periodic tasks reliably at 5-minute intervals
- **No External Dependencies**: No Redis/RabbitMQ broker needed
- **Easy Monitoring**: Logs directly to application logs
- **Migration Path**: Can switch to Celery later if needed

### Alternatives Considered
- **Celery**: Industry standard, but requires Redis/RabbitMQ broker (adds complexity)
- **Cron Jobs**: External to application, harder to coordinate with app state
- **Background Tasks (FastAPI)**: Good for one-off tasks, not periodic scheduling
- **Temporal**: Powerful workflow engine, but overkill for simple periodic tasks

### Implementation Notes
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = AsyncIOScheduler()

# News scraping every 5 minutes
scheduler.add_job(
    fetch_all_news_feeds,
    trigger=IntervalTrigger(minutes=5),
    id="news_scraper",
    replace_existing=True
)

# File cleanup daily at 2 AM
scheduler.add_job(
    cleanup_expired_exports,
    trigger="cron",
    hour=2,
    minute=0,
    id="file_cleanup"
)

scheduler.start()
```

### When to Migrate to Celery
- More than 10 background job types
- Jobs taking longer than 30 seconds
- Need for distributed task processing
- Require task priorities or queues

---

## Decision 7: Authentication Strategy

### Decision
**JWT tokens with httpOnly cookies** for authentication

### Rationale
- **Stateless**: No server-side session storage needed (enables horizontal scaling)
- **Secure**: httpOnly cookies prevent XSS attacks (can't access via JavaScript)
- **Standard**: Industry best practice for modern web apps
- **Flexible**: Can add refresh tokens later if needed
- **Simple**: Python libraries (python-jose, passlib) make implementation easy

### Alternatives Considered
- **Session Cookies**: Simpler, but requires Redis session storage
- **OAuth2**: More complex, overkill for MVP without third-party login
- **API Keys**: Good for API access, but not ideal for web UI
- **localStorage JWT**: Common but vulnerable to XSS attacks

### Implementation Notes
```python
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # 256-bit random
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]  # Returns user_id

# FastAPI dependency
async def get_current_user(token: str = Cookie(None)) -> User:
    if not token:
        raise HTTPException(status_code=401)
    user_id = verify_token(token)
    return await get_user_by_id(user_id)
```

### Security Measures
- bcrypt with cost factor 12 for password hashing
- HTTPS only (no HTTP)
- CSRF protection for state-changing operations
- Short token expiration (24 hours)
- Token rotation on sensitive operations
- Rate limiting on login attempts (5 attempts per 15 minutes)

---

## Decision 8: Frontend Framework

### Decision
**Vanilla HTML, CSS, JavaScript** (no framework)

### Rationale
- **Simplicity**: No build tooling, bundlers, or compilation needed
- **Fast Development**: Direct HTML/CSS/JS editing with instant refresh
- **Small Bundle**: No framework overhead (faster page loads)
- **Easy Debugging**: Inspect source code directly in browser DevTools
- **Sufficient for MVP**: UI complexity doesn't justify framework overhead
- **Migration Path**: Can add React/Vue later if UI complexity grows

### Alternatives Considered
- **React**: Most popular, but adds build complexity and bundle size
- **Vue**: Simpler than React, but still requires build step
- **Svelte**: Great DX, but less mature ecosystem
- **Alpine.js**: Lightweight, good middle ground (consider for future)

### Implementation Approach
```javascript
// Modern vanilla JS patterns
class DocumentUploader {
  constructor(elementId) {
    this.element = document.getElementById(elementId);
    this.setupEventListeners();
  }
  
  setupEventListeners() {
    this.element.addEventListener('drop', this.handleDrop.bind(this));
    this.element.addEventListener('dragover', this.handleDragOver.bind(this));
  }
  
  async handleDrop(e) {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    await this.uploadFile(file);
  }
  
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/documents/upload', {
      method: 'POST',
      body: formData,
      credentials: 'include'  // Include cookies
    });
    
    const data = await response.json();
    this.onUploadComplete(data);
  }
}

// Usage
const uploader = new DocumentUploader('upload-zone');
```

### CSS Strategy
- Use CSS Grid and Flexbox for layouts
- CSS custom properties for theming
- Mobile-first responsive design (320px+)
- No CSS preprocessors (Sass/Less) for MVP

---

## Decision 9: RAG Architecture

### Decision
**LangChain + Groq + ChromaDB** for RAG pipeline

### Rationale
- **LangChain**: Industry standard for RAG, handles retrieval → generation flow
- **Modular**: Can swap components (embeddings, LLMs, vector stores) easily
- **Well-Documented**: Extensive examples and community support
- **Agent Support**: Can build conversational agents for stock queries
- **Memory**: Built-in conversation memory for follow-up questions

### RAG Pipeline Design
```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatGroq
from langchain.chains import RetrievalQA

# 1. Text chunking
def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50):
    """Split text into overlapping chunks"""
    # Implementation using RecursiveCharacterTextSplitter
    pass

# 2. Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. Vector store
vectorstore = Chroma(
    collection_name=f"doc_{document_id}",
    embedding_function=embeddings,
    persist_directory="./chroma_data"
)

# 4. Retrieval
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Top 5 chunks
)

# 5. LLM
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.7,
    groq_api_key=os.environ["GROQ_API_KEY"]
)

# 6. Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Simple concatenation
    retriever=retriever,
    return_source_documents=True  # For citations
)

# 7. Query
result = qa_chain({"query": "What was Q4 revenue?"})
answer = result["result"]
sources = result["source_documents"]  # For page citations
```

### Optimization Strategies
- Cache embeddings in memory (don't recompute)
- Use smaller embedding model for speed (all-MiniLM-L6-v2)
- Limit retrieval to top 5 chunks
- Implement timeout (10 seconds max)
- Add retry logic with exponential backoff

---

## Open Questions & Future Research

### Scalability Concerns
- **Q**: How does ChromaDB perform with 100K+ documents?
- **A**: To be determined through load testing; may need migration to client-server mode

### Model Selection
- **Q**: Should we use different Groq models for different tasks?
- **A**: Start with Mixtral for everything; evaluate task-specific models in Phase 7

### Caching Strategy
- **Q**: What should be cached and for how long?
- **A**: News articles (1 hour), summaries (24 hours), stock data (5 minutes), embeddings (indefinitely)

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Backend Framework** | FastAPI | Modern, fast, great developer experience |
| **Language** | Python 3.9+ | Rich AI/ML ecosystem |
| **LLM Provider** | Groq | Fastest inference, cost-effective |
| **Vector Database** | ChromaDB | Embedded, simple, Python-native |
| **Relational DB** | PostgreSQL | Reliable, feature-rich, open-source |
| **Cache/Sessions** | Redis | Fast, widely used, simple |
| **Email Service** | Gmail SMTP | Free, reliable, easy setup |
| **Blob Storage** | Local Filesystem | Zero cost MVP, easy migration to S3 |
| **Frontend** | Vanilla HTML/CSS/JS | Simple, no build step, fast |
| **News Parsing** | RSS Feeds + feedparser | Free, reliable, structured |
| **Stock Data** | yfinance | Free, real-time, easy API |
| **Background Jobs** | APScheduler | Simple, no broker needed |
| **Authentication** | JWT + bcrypt | Secure, stateless, standard |
| **OCR** | Poppler + pytesseract | Open-source, good accuracy |
| **PDF Export** | WeasyPrint | HTML to PDF, CSS styling |
| **DOCX Export** | python-docx | Word-compatible docs |

---

**Research Completion Date**: 2025-10-28  
**Next Steps**: Begin implementation following plan.md phases  
**Review Schedule**: Revisit decisions quarterly or when requirements change

