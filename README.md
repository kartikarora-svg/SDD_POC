# Finalytics MVP Platform

**Version**: 1.0.0  
**Status**: In Development

## Overview

Finalytics is a web-based financial analytics platform that empowers users with intelligent, real-time financial insights through advanced document analysis, live market data integration, and AI-powered natural language interaction.

### Core Features

- 📄 **Document Intelligence**: Upload financial documents (PDFs) and ask questions powered by AI
- 📰 **Real-Time News**: Live financial news feed with AI-generated summaries
- 📈 **Stock Research**: Natural language queries for real-time stock data via Yahoo Finance
- ⚖️ **Stock Comparison**: Side-by-side analysis of any two stocks with AI insights
- 📤 **Export & Sharing**: Export analyses as PDF/DOCX or share via email

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.9+
- **Database**: PostgreSQL 14+
- **Cache**: Redis 7+
- **Vector DB**: ChromaDB
- **ORM**: SQLAlchemy + Alembic

### AI/ML
- **LLM Provider**: Groq
- **RAG Framework**: LangChain
- **OCR**: Poppler + PyTesseract

### Frontend
- **Stack**: Vanilla HTML/CSS/JavaScript
- **Design**: Responsive, mobile-first

## Quick Start

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 14+
- Redis 7+
- Tesseract OCR
- Poppler utils

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Finalytics
```

2. **Start infrastructure (using Docker)**
```bash
docker-compose up -d
```

3. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment**
```bash
cp env.example .env
# Edit .env with your configuration
```

6. **Run database migrations**
```bash
alembic upgrade head
```

7. **Start the application**
```bash
python -m app.main
```

8. **Access the application**
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/health

## Project Structure

```
Finalytics/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database session management
│   ├── redis_client.py      # Redis client setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic services
│   ├── utils/               # Utility functions
│   └── middleware/          # Custom middleware
├── alembic/                 # Database migrations
├── static/                  # Frontend files
│   ├── css/
│   ├── js/
│   └── images/
├── storage/                 # Uploaded files (gitignored)
├── chroma_data/            # ChromaDB vector storage (gitignored)
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Infrastructure setup
└── README.md               # This file
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Linting
```bash
flake8 app/
```

### Creating Migrations
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Configuration

Key environment variables (see `env.example`):

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `GROQ_API_KEY`: Groq API key for LLM
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `SMTP_USERNAME`: Gmail username for email sharing
- `SMTP_PASSWORD`: Gmail app-specific password

## Constitutional Principles

This project adheres to 5 core constitutional principles:

1. **On-Demand Document Intelligence**: Instant RAG-powered document Q&A
2. **Actionable & Shareable Analysis**: Easy export and email sharing
3. **Real-Time Market Awareness**: Live news feed with AI summaries
4. **Live Ticker RAG Agent**: Conversational stock data access
5. **Seamless Comparative Analysis**: Side-by-side stock comparison

See `.specify/memory/constitution.md` for complete governance framework.

## Implementation Status

### Phase 1: Project Setup ✅ COMPLETED
- [x] Project structure created
- [x] Dependencies configured
- [x] Environment setup
- [x] Database and Redis initialization
- [x] Frontend structure created

### Phase 2: Authentication (In Progress)
- [ ] User model
- [ ] JWT authentication
- [ ] Login/Register API
- [ ] Auth UI

### Remaining Phases
- Phase 3: Document Intelligence
- Phase 4: Export & Sharing
- Phase 5: News Feed
- Phase 6: Stock Research
- Phase 7: Stock Comparison
- Phase 8: Polish & Deployment

## Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting PR

## License

Proprietary - All rights reserved

## Support

For issues and questions, please refer to the project documentation in `/specs/001-platform-mvp/`.

---

**Built with ❤️ for financial analysts, investors, and traders**
