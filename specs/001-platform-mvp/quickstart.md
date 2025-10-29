# Finalytics MVP - Developer Quickstart Guide

**Goal**: Get a fully functional local development environment running in under 30 minutes

**Last Updated**: 2025-10-28

---

## Prerequisites

Before starting, ensure you have the following installed:

- [ ] **Python 3.9+**: `python --version` should show 3.9 or higher
- [ ] **PostgreSQL 14+**: `psql --version`
- [ ] **Redis 7+**: `redis-cli --version`
- [ ] **Git**: `git --version`
- [ ] **Poppler**: PDF processing utilities
  - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows)
  - **Mac**: `brew install poppler`
  - **Linux**: `sudo apt-get install poppler-utils tesseract-ocr`

---

## Step 1: Clone and Setup Project (5 minutes)

```bash
# Clone the repository
git clone https://github.com/your-org/finalytics.git
cd finalytics

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi  # Should show FastAPI installed
```

---

## Step 2: Database Setup (5 minutes)

### PostgreSQL

```bash
# Start PostgreSQL (if not running)
# Windows: Use Services app or pgAdmin
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
psql -U postgres

CREATE DATABASE finalytics;
CREATE USER finalytics_user WITH PASSWORD 'dev_password_123';
GRANT ALL PRIVILEGES ON DATABASE finalytics TO finalytics_user;
\q
```

### Redis

```bash
# Start Redis (if not running)
# Windows: redis-server.exe
# Mac: brew services start redis
# Linux: sudo systemctl start redis

# Verify Redis is running
redis-cli ping  # Should return PONG
```

---

## Step 3: Environment Configuration (3 minutes)

Create a `.env` file in the project root:

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database
DATABASE_URL=postgresql://finalytics_user:dev_password_123@localhost:5432/finalytics

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Secret (generate a random 256-bit key)
JWT_SECRET_KEY=your-secret-key-here-change-this-in-production

# Groq API (get from https://console.groq.com/)
GROQ_API_KEY=gsk_your_api_key_here

# Gmail SMTP (optional for Phase 3+)
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-specific-password

# Storage
STORAGE_PATH=./storage

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_data

# App Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

**Important**: Get your Groq API key from [https://console.groq.com/](https://console.groq.com/) (free tier available)

---

## Step 4: Run Database Migrations (2 minutes)

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head

# Verify tables were created
psql -U finalytics_user -d finalytics -c "\dt"
# Should show: users, documents, query_history, news_articles, etc.
```

---

## Step 5: Start the Application (2 minutes)

```bash
# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Verify the server is running**:
- Open browser to [http://localhost:8000](http://localhost:8000)
- Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI)
- Visit [http://localhost:8000/health](http://localhost:8000/health) for health check

---

## Step 6: Test Basic Functionality (5 minutes)

### Register a Test User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'

# Should return:
# {
#   "status": "success",
#   "data": {
#     "user_id": "...",
#     "email": "test@example.com",
#     "token": "eyJ..."
#   }
# }
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }' \
  -c cookies.txt  # Save cookies for subsequent requests

# Should return JWT token
```

### Upload a Test Document (Phase 2+)

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./test_data/sample_10k.pdf" \
  -b cookies.txt  # Use saved cookies

# Should return document_id and status: "processing"
```

---

## Step 7: Access the Frontend (2 minutes)

```bash
# Frontend files are served from static/ directory
# Open browser to:
http://localhost:8000/

# You should see:
# - Login/Register page
# - Navigation to Dashboard, Documents, News, Stocks, Compare

# Login with your test credentials:
# Email: test@example.com
# Password: TestPassword123!
```

---

## Development Workflow

### Running the Application

```bash
# Start backend (with auto-reload)
uvicorn app.main:app --reload

# In a separate terminal, start background jobs (Phase 4+)
python app/workers/scheduler.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_user_registration
```

### Database Management

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Reset database (CAUTION: destroys all data)
alembic downgrade base
alembic upgrade head
```

### Code Formatting and Linting

```bash
# Format code with black
black app/ tests/

# Sort imports
isort app/ tests/

# Lint with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/
```

---

## Project Structure

```
finalytics/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── database.py          # SQLAlchemy setup and session management
│   ├── models/              # SQLAlchemy models (User, Document, etc.)
│   ├── schemas/             # Pydantic schemas for validation
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # /api/auth/* endpoints
│   │   ├── documents.py     # /api/documents/* endpoints
│   │   ├── news.py          # /api/news/* endpoints
│   │   ├── stocks.py        # /api/stocks/* endpoints
│   │   └── exports.py       # /api/export/* endpoints
│   ├── services/            # Business logic services
│   │   ├── document_service.py    # OCR, RAG, Q&A
│   │   ├── export_service.py      # PDF, DOCX, Email
│   │   ├── news_service.py        # RSS scraping, summarization
│   │   └── stock_service.py       # yfinance, comparison
│   ├── workers/             # Background jobs
│   │   └── scheduler.py     # APScheduler setup
│   └── utils/               # Helper functions
│       ├── auth.py          # JWT, password hashing
│       ├── storage.py       # File storage abstraction
│       └── rag.py           # RAG pipeline utilities
├── static/                  # Frontend files
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── app.js
│       ├── auth.js
│       ├── documents.js
│       └── stocks.js
├── tests/                   # Test files
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py
│   ├── test_documents.py
│   └── test_stocks.py
├── alembic/                 # Database migrations
│   └── versions/
├── storage/                 # Local file storage (created at runtime)
├── chroma_data/             # ChromaDB persistence (created at runtime)
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── specs/                   # Specification documents
    └── 001-platform-mvp/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md (this file)
        └── contracts/
```

---

## Common Issues and Solutions

### Issue: PostgreSQL connection refused

**Solution**:
```bash
# Check if PostgreSQL is running
# Windows: Check Services
# Mac: brew services list
# Linux: sudo systemctl status postgresql

# Start PostgreSQL if not running
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### Issue: Redis connection error

**Solution**:
```bash
# Check if Redis is running
redis-cli ping

# If not running, start it
# Mac: brew services start redis
# Linux: sudo systemctl start redis
# Windows: redis-server.exe
```

### Issue: Groq API key not working

**Solution**:
1. Verify your API key at [https://console.groq.com/](https://console.groq.com/)
2. Ensure `.env` file has correct key: `GROQ_API_KEY=gsk_...`
3. Restart the server after updating `.env`

### Issue: Poppler not found (OCR errors)

**Solution**:
```bash
# Verify Poppler is installed
pdftoppm -v

# If not found, install Poppler
# Mac: brew install poppler
# Linux: sudo apt-get install poppler-utils
# Windows: Download from GitHub and add to PATH
```

### Issue: Module not found errors

**Solution**:
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Alembic migration conflicts

**Solution**:
```bash
# Reset to a clean state
alembic downgrade base
alembic upgrade head

# If that fails, drop and recreate database
dropdb finalytics
createdb finalytics
alembic upgrade head
```

---

## Next Steps

Once your local environment is running:

1. **Explore the API**: Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger documentation
2. **Read the Spec**: Review `specs/001-platform-mvp/spec.md` for feature details
3. **Check the Plan**: See `specs/001-platform-mvp/plan.md` for implementation phases
4. **Review Data Models**: Read `specs/001-platform-mvp/data-model.md` for database schema
5. **Understand Research**: See `specs/001-platform-mvp/research.md` for technical decisions

---

## Getting Help

- **Documentation**: Check the `specs/` directory for detailed specifications
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs) for endpoint documentation
- **Issues**: Report bugs or ask questions in the GitHub issues
- **Team**: Contact the Finalytics engineering team on Slack

---

## Production Deployment Notes

This quickstart is for **local development only**. For production deployment:

- Use production-grade database (managed PostgreSQL)
- Set up Redis cluster for high availability
- Migrate from local filesystem to S3/Azure Blob Storage
- Use proper secrets management (AWS Secrets Manager, Azure Key Vault)
- Enable HTTPS with valid SSL certificates
- Set `DEBUG=False` in production
- Use Gunicorn/Uvicorn workers for concurrency
- Set up monitoring and alerting
- Implement rate limiting and DDoS protection
- Use CDN for static assets

**DO NOT use this setup in production without proper security hardening!**

---

**Estimated Setup Time**: 25-30 minutes  
**Support**: engineering@finalytics.io  
**Last Updated**: 2025-10-28

