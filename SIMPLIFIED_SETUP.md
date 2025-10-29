# Finalytics - Simplified Setup ✨

**No Docker Required!** This project now uses SQLite for maximum simplicity.

## Quick Start (3 Steps)

### 1. Install Dependencies
```powershell
cd C:\Users\kartik.arora\SDD\Finalytics
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-py313.txt
pip install pydantic[email]
```

### 2. Create Database
```powershell
alembic upgrade head
```

### 3. Start Server
```powershell
python -m app.main
```

Visit: **http://localhost:8000**

## What's Working Right Now

✅ **Authentication System**
- User registration (email + password)
- Login with JWT tokens
- Protected API endpoints
- SQLite database (`finalytics.db`)

✅ **Frontend**
- Responsive UI
- Login/Register pages
- Dashboard navigation

## Tech Stack

| Component | Technology | Why? |
|-----------|------------|------|
| **Backend** | FastAPI | Fast, modern Python API |
| **Database** | SQLite | No Docker needed! |
| **Auth** | JWT + Bcrypt | Secure tokens |
| **Frontend** | Vanilla JS | No build step |
| **LLM** | Groq | Free, fast AI |

## What's Next (Phase 3)

We're building **Document Intelligence**:
1. PDF upload
2. OCR text extraction
3. AI-powered Q&A
4. Export results

## Configuration

All settings in `app/config.py` - defaults work out of the box!

Optional: Create `.env` file for customization:
```
GROQ_API_KEY=your-key-here
DEBUG=true
```

## Database Location

- **File**: `finalytics.db` (in project root)
- **View**: Use [DB Browser for SQLite](https://sqlitebrowser.org/)
- **Reset**: Just delete `finalytics.db` and run `alembic upgrade head`

## No Redis Needed

Redis was for caching. We'll add it later if needed. For now, everything works without it!

## Common Issues

### "Module not found"
```powershell
pip install pydantic[email]
```

### "Database is locked"
Close all database viewers and restart server.

### "Server won't start"
Check port 8000 isn't in use:
```powershell
netstat -ano | findstr :8000
```

## Project Status

| Phase | Status | Progress |
|-------|--------|----------|
| ✅ Phase 1: Setup | DONE | 100% |
| ✅ Phase 2: Auth | DONE | 100% |
| 🔄 Phase 3: Documents | IN PROGRESS | 0% |

**Simplified!** No Docker, no PostgreSQL, no complex setup. Just Python and SQLite!

