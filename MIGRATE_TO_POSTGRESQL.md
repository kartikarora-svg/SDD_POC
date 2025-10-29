# 🚀 PostgreSQL Migration Guide

This guide helps you migrate from SQLite to PostgreSQL in the `feature/nextjs-frontend` branch.

---

## Why Migrate to PostgreSQL?

### Advantages Over SQLite

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Concurrent Writes** | ❌ Single writer | ✅ Multiple concurrent writers |
| **Production Scale** | ⚠️ Limited | ✅ Handles millions of rows |
| **JSON Support** | ⚠️ Basic | ✅ Advanced JSON/JSONB queries |
| **Full-Text Search** | ⚠️ Limited | ✅ Native FTS with ranking |
| **Backup/Replication** | ⚠️ File copy only | ✅ Point-in-time recovery, streaming replication |
| **User Management** | ❌ No users | ✅ Role-based access control |
| **Performance** | ✅ Great for <100K rows | ✅ Great for millions+ rows |

### When to Use Each

- **SQLite**: Local development, demos, single-user apps, embedded systems
- **PostgreSQL**: Production deployments, multiple users, high traffic, enterprise applications

---

## 🔧 Migration Steps

### Step 1: Install PostgreSQL

#### Option A: Docker (Recommended for Development)

```bash
# Pull PostgreSQL image
docker pull postgres:16-alpine

# Run PostgreSQL container
docker run --name finalytics-postgres \
  -e POSTGRES_USER=finalytics_user \
  -e POSTGRES_PASSWORD=secure_password_here \
  -e POSTGRES_DB=finalytics \
  -p 5432:5432 \
  -v finalytics_pgdata:/var/lib/postgresql/data \
  -d postgres:16-alpine

# Verify it's running
docker ps | grep finalytics-postgres
```

**Windows PowerShell**:
```powershell
docker run --name finalytics-postgres `
  -e POSTGRES_USER=finalytics_user `
  -e POSTGRES_PASSWORD=secure_password_here `
  -e POSTGRES_DB=finalytics `
  -p 5432:5432 `
  -v finalytics_pgdata:/var/lib/postgresql/data `
  -d postgres:16-alpine
```

#### Option B: Native Installation

**Windows**:
1. Download installer: https://www.postgresql.org/download/windows/
2. Run installer (default port 5432)
3. Remember the password you set for postgres user
4. Add `C:\Program Files\PostgreSQL\16\bin` to PATH

**macOS**:
```bash
brew install postgresql@16
brew services start postgresql@16
createuser -s finalytics_user
createdb finalytics -O finalytics_user
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createuser finalytics_user
sudo -u postgres createdb finalytics -O finalytics_user
```

---

### Step 2: Verify PostgreSQL Driver

The PostgreSQL driver (`psycopg`) is already in `requirements.txt`. Verify it's installed:

```bash
# In your virtual environment
pip list | grep psycopg
```

**Expected output**:
```
psycopg                3.1.13
psycopg-binary         3.1.13
psycopg-pool           3.2.0
```

If not installed:
```bash
pip install psycopg[binary]==3.1.13 psycopg-pool==3.2.0
```

---

### Step 3: Update Environment Configuration

Edit your `.env` file (or create from `env.example`):

```bash
# Change FROM (SQLite):
DATABASE_URL=sqlite:///./finalytics.db

# Change TO (PostgreSQL):
DATABASE_URL=postgresql://finalytics_user:secure_password_here@localhost:5432/finalytics
```

**Connection String Format**:
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Example values**:
- `user`: finalytics_user
- `password`: Your secure password
- `host`: localhost (or IP address if remote)
- `port`: 5432 (default PostgreSQL port)
- `database`: finalytics

---

### Step 4: Run Database Migrations

Your code is already PostgreSQL-ready thanks to SQLAlchemy! Just run migrations:

```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Run Alembic migrations
alembic upgrade head
```

**Expected output**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_create_users_table
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002_add_documents_and_query_history
...
```

---

### Step 5: (Optional) Migrate Existing Data

If you have existing data in SQLite that you want to migrate:

#### Option A: Manual Export/Import (Small Dataset)

```bash
# 1. Export from SQLite
python scripts/export_sqlite_data.py

# 2. Import to PostgreSQL
python scripts/import_to_postgresql.py
```

#### Option B: Use pgloader (Automatic)

```bash
# Install pgloader
# macOS: brew install pgloader
# Ubuntu: sudo apt install pgloader

# Create migration script
cat > migrate.load <<EOF
LOAD DATABASE
     FROM sqlite:///finalytics.db
     INTO postgresql://finalytics_user:secure_password_here@localhost:5432/finalytics
     WITH data only
     INCLUDING ONLY TABLE NAMES MATCHING ~<users|documents|news_articles|exports|stock_queries|stock_comparisons>
     SET work_mem TO '256MB', maintenance_work_mem TO '512 MB';
EOF

# Run migration
pgloader migrate.load
```

---

### Step 6: Verify Migration

Test the application to ensure everything works:

```bash
# Start FastAPI backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Test checklist**:
- ✅ Register a new user
- ✅ Login successfully
- ✅ Upload a document
- ✅ Ask questions about the document
- ✅ Scrape news articles
- ✅ Query stock data
- ✅ Compare two stocks
- ✅ Check that data persists after restart

---

## 📊 Performance Optimization

### Create Indexes for Better Query Performance

Connect to PostgreSQL:
```bash
psql -U finalytics_user -d finalytics
```

Create indexes:
```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email);

-- Document queries
CREATE INDEX idx_documents_user_status ON documents(user_id, status);
CREATE INDEX idx_documents_created ON documents(created_at DESC);

-- News articles
CREATE INDEX idx_news_source_published ON news_articles(source, published_at DESC);
CREATE INDEX idx_news_scraped ON news_articles(scraped_at DESC);

-- Query history
CREATE INDEX idx_query_history_document ON query_history(document_id, created_at DESC);

-- Stock comparisons
CREATE INDEX idx_stock_comparisons_user ON stock_comparisons(user_id, compared_at DESC);

-- Full-text search on documents (optional)
CREATE INDEX idx_documents_text_fts ON documents USING gin(to_tsvector('english', extracted_text));
```

---

## 🔄 Switching Between SQLite and PostgreSQL

Your code supports **both databases** simultaneously! Just change the `DATABASE_URL`:

### Use SQLite (Development)
```bash
# .env
DATABASE_URL=sqlite:///./finalytics.db
```

### Use PostgreSQL (Production)
```bash
# .env
DATABASE_URL=postgresql://finalytics_user:password@localhost:5432/finalytics
```

**No code changes needed** - SQLAlchemy handles everything!

---

## 🐳 Docker Compose for Easy Setup

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: finalytics-postgres
    environment:
      POSTGRES_USER: finalytics_user
      POSTGRES_PASSWORD: secure_password_here
      POSTGRES_DB: finalytics
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=en_US.utf8"
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U finalytics_user -d finalytics"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
```

**Usage**:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Stop PostgreSQL
docker-compose down

# View logs
docker-compose logs -f postgres

# Access PostgreSQL shell
docker-compose exec postgres psql -U finalytics_user -d finalytics
```

---

## 🛠️ Troubleshooting

### Issue: "Could not connect to server"

**Check if PostgreSQL is running**:
```bash
# Docker
docker ps | grep postgres

# Native (Windows)
Get-Service postgresql*

# Native (macOS/Linux)
sudo systemctl status postgresql
# or
ps aux | grep postgres
```

**Solution**: Start PostgreSQL service or Docker container.

---

### Issue: "FATAL: password authentication failed"

**Check credentials**:
```bash
# Test connection
psql -U finalytics_user -d finalytics -h localhost
```

**Solution**: Verify username/password in `DATABASE_URL` matches PostgreSQL user.

---

### Issue: "database 'finalytics' does not exist"

**Create the database**:
```bash
# Connect as postgres superuser
psql -U postgres

# Create database
CREATE DATABASE finalytics OWNER finalytics_user;

# Exit
\q
```

---

### Issue: Slow queries after migration

**Solutions**:
1. **Analyze tables** to update statistics:
   ```sql
   ANALYZE users;
   ANALYZE documents;
   ANALYZE news_articles;
   ```

2. **Vacuum database** to optimize:
   ```sql
   VACUUM ANALYZE;
   ```

3. **Add indexes** (see Performance Optimization section above)

---

## 📈 Monitoring PostgreSQL

### Connection Pool Stats

In your Python code:
```python
from app.database import engine

# Check pool status
print(f"Pool size: {engine.pool.size()}")
print(f"Checked out connections: {engine.pool.checkedout()}")
print(f"Overflow: {engine.pool.overflow()}")
```

### PostgreSQL Query Performance

```sql
-- Show active queries
SELECT pid, usename, application_name, state, query 
FROM pg_stat_activity 
WHERE state = 'active';

-- Show slow queries
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- Show table sizes
SELECT 
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 🔐 Security Best Practices

### 1. Use Strong Password
```bash
# Generate secure password
openssl rand -base64 32
```

### 2. Restrict Network Access
Edit `postgresql.conf` and `pg_hba.conf`:
```
# Allow only localhost
listen_addresses = 'localhost'
```

### 3. Use SSL/TLS in Production
```bash
# Connection string with SSL
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

### 4. Regular Backups
```bash
# Backup database
pg_dump -U finalytics_user finalytics > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U finalytics_user finalytics < backup_20250129.sql
```

---

## 🎯 Summary

✅ **You can now easily switch between SQLite and PostgreSQL** by changing one environment variable!

### Quick Command Reference

```bash
# Start PostgreSQL (Docker)
docker-compose up -d postgres

# Update .env
DATABASE_URL=postgresql://finalytics_user:password@localhost:5432/finalytics

# Run migrations
alembic upgrade head

# Start FastAPI
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Test everything works
curl http://localhost:8000/api/health
```

---

## 📚 Additional Resources

- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [psycopg3 Documentation](https://www.psycopg.org/psycopg3/docs/)

---

**Questions or Issues?** Check the troubleshooting section or create an issue in the repository.

🎉 **Happy migrating!**

