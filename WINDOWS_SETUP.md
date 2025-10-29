# Windows Setup Guide for Finalytics

This guide provides Windows-specific installation instructions for the Finalytics platform.

## Prerequisites

### 1. Python 3.11 or 3.12 (Recommended)
Download from: https://www.python.org/downloads/

**⚠️ IMPORTANT**: 
- **Recommended**: Python 3.11.x or 3.12.x (best package compatibility)
- **Not Recommended**: Python 3.13+ (too new, many packages lack pre-built wheels)
- **Minimum**: Python 3.9+

**Installation Tips**:
- Check "Add Python to PATH" during installation
- Check "Install for all users" (optional but helpful)

Verify installation:
```powershell
python --version
# Should show: Python 3.11.x or 3.12.x
```

### 2. Docker Desktop (Recommended)
Download from: https://www.docker.com/products/docker-desktop/

This provides PostgreSQL and Redis without manual installation.

### 3. Tesseract OCR (Optional - for document OCR)
Download from: https://github.com/UB-Mannheim/tesseract/wiki

Add to PATH or set in `.env`:
```
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### 4. Poppler (Optional - for PDF processing)
Download from: https://github.com/oschwartz10612/poppler-windows/releases/

1. Extract to `C:\Program Files\poppler`
2. Add `C:\Program Files\poppler\Library\bin` to PATH

---

## Installation Steps

### Step 1: Clone Repository
```powershell
git clone <repository-url>
cd Finalytics
```

### Step 2: Start Infrastructure
```powershell
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379

Verify with:
```powershell
docker ps
```

### Step 3: Create Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### Step 4: Install Dependencies

**Check your Python version first**:
```powershell
python --version
```

**If Python 3.13+** (too new, limited package support):
```powershell
pip install --upgrade pip
pip install -r requirements-py313.txt
```

**If Python 3.9-3.12** (recommended):
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**If you get compilation errors**, use the updated requirements:
```powershell
pip install -r requirements-py313.txt
```

**Optional Windows-specific libraries:**

If you need WeasyPrint for PDF export:
```powershell
# Install GTK3 runtime first from:
# https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

pip install WeasyPrint
```

If you get errors with any AI libraries, install them separately:
```powershell
pip install langchain chromadb groq
```

### Step 5: Configure Environment
```powershell
copy env.example .env
```

Edit `.env` with your settings:
- Get Groq API key from: https://console.groq.com/
- Configure Gmail SMTP (use app-specific password)

### Step 6: Verify Setup
```powershell
python verify_setup.py
```

This checks:
- ✓ All Python packages imported
- ✓ Configuration loaded
- ✓ Database connection
- ✓ Redis connection
- ✓ FastAPI app created

### Step 7: Run Database Migrations
```powershell
alembic upgrade head
```

### Step 8: Start Server
```powershell
python -m app.main
```

Access:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/health

---

## Common Issues & Solutions

### Issue 1: Python 3.13 Compilation Errors (pydantic-core needs Rust)
**Error**: `Cargo, the Rust package manager, is not installed`

**Root Cause**: Python 3.13 is too new; many packages lack pre-built wheels

**Solutions** (choose one):

**Option A - Use Updated Requirements** (Quickest):
```powershell
pip install -r requirements-py313.txt
```

**Option B - Downgrade Python** (Recommended for best compatibility):
1. Uninstall Python 3.13
2. Download Python 3.12.x from https://www.python.org/downloads/
3. Reinstall and recreate virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Option C - Install Rust** (If you want to keep Python 3.13):
```powershell
# Install Rust from https://rustup.rs/
# OR use winget:
winget install Rustlang.Rustup

# Restart terminal, then:
pip install -r requirements.txt
```

### Issue 2: `psycopg2-binary` Installation Error
**Solution**: Already fixed! We use `psycopg` v3 which has pre-built Windows wheels.

### Issue 3: ChromaDB SQLite Error
**Error**: `no such module: fts5`

**Solution**: Install latest SQLite:
```powershell
pip install pysqlite3-binary
```

### Issue 4: WeasyPrint Installation Fails
**Solution**: WeasyPrint requires GTK3 runtime on Windows.

**Option A** - Use ReportLab instead (already in requirements):
```python
# In export service, use reportlab instead of WeasyPrint
from reportlab.pdfgen import canvas
```

**Option B** - Install GTK3:
1. Download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Install to `C:\Program Files\GTK3-Runtime Win64`
3. Then: `pip install WeasyPrint`

### Issue 5: Poppler Not Found (pdf2image error)
**Error**: `PDFInfoNotInstalledError: Unable to get page count`

**Solution**:
1. Download Poppler for Windows
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to system PATH
4. Restart terminal

**OR** set in `.env`:
```
POPPLER_PATH=C:\Program Files\poppler\Library\bin
```

### Issue 6: Tesseract Not Found (pytesseract error)
**Error**: `TesseractNotFoundError`

**Solution**:
1. Download Tesseract installer
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add to PATH or set in `.env`:
```
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Issue 7: Docker Connection Errors
**Error**: `Cannot connect to the Docker daemon`

**Solution**:
1. Start Docker Desktop
2. Wait for "Docker Desktop is running" notification
3. Run: `docker-compose up -d`

### Issue 8: Port Already in Use
**Error**: `Port 5432 is already allocated`

**Solution**: Stop existing PostgreSQL/Redis:
```powershell
# Stop all containers
docker stop $(docker ps -q)

# Or change ports in docker-compose.yml:
ports:
  - "5433:5432"  # Use 5433 instead

# Update DATABASE_URL in .env accordingly
```

---

## Development Workflow

### Start Development Session
```powershell
# Terminal 1: Start infrastructure
docker-compose up

# Terminal 2: Start application
.venv\Scripts\activate
python -m app.main
```

### Stop Development Session
```powershell
# Ctrl+C to stop server

# Stop Docker containers
docker-compose down
```

### Run Tests
```powershell
pytest
```

### Code Formatting
```powershell
black app/
flake8 app/
```

---

## Performance Tips for Windows

1. **Use WSL2 for Docker**: Better performance than Hyper-V
2. **Exclude folders from Windows Defender**:
   - `.venv`
   - `node_modules` (if using Node)
   - `chroma_data`
   - `storage`
3. **Use PowerShell 7**: Faster than Windows PowerShell
4. **SSD recommended**: Database and vector storage benefit from SSD

---

## Troubleshooting Commands

### Check Python Version
```powershell
python --version
```

### Check Installed Packages
```powershell
pip list
```

### Check Docker Status
```powershell
docker ps
docker-compose ps
```

### Check PostgreSQL Connection
```powershell
docker exec -it finalytics-postgres psql -U postgres -d finalytics
```

### Check Redis Connection
```powershell
docker exec -it finalytics-redis redis-cli ping
```

### View Application Logs
```powershell
# Docker logs
docker-compose logs -f

# Application logs (if running directly)
python -m app.main 2>&1 | Tee-Object -FilePath app.log
```

---

## Alternative: Manual PostgreSQL/Redis Installation

If you prefer not to use Docker:

### PostgreSQL
1. Download: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Create database:
```sql
CREATE DATABASE finalytics;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE finalytics TO postgres;
```

### Redis
1. Download: https://github.com/microsoftarchive/redis/releases
2. Install as Windows Service
3. Or use Memurai (Redis alternative): https://www.memurai.com/

Update `.env`:
```
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/finalytics
REDIS_URL=redis://localhost:6379/0
```

---

## Next Steps

Once setup is complete:
1. ✅ All dependencies installed
2. ✅ Infrastructure running
3. ✅ Configuration set
4. ✅ Server starts successfully

Continue to **Phase 2: Authentication** implementation!

---

## Need Help?

- Check `README.md` for general documentation
- Run `python verify_setup.py` to diagnose issues
- Check `IMPLEMENTATION_LOG.md` for progress tracking

---

*Windows-specific setup guide | Last updated: 2025-10-28*

