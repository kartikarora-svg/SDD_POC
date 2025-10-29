# 🚀 Quick Reference Card: Database Operations

**Branch**: `feature/nextjs-frontend` (PostgreSQL-ready)  
**Main Branch**: `main` (SQLite-only)

---

## ⚡ One-Line Commands

### **Start with SQLite (Default)**
```bash
DATABASE_URL=sqlite:///./finalytics.db uvicorn app.main:app --reload
```

### **Start with PostgreSQL**
```bash
# Start PostgreSQL first
docker-compose up -d postgres

# Then start FastAPI
DATABASE_URL=postgresql://finalytics_user:secure_password_change_me@localhost:5432/finalytics uvicorn app.main:app --reload
```

---

## 🔄 Switch Databases

### **SQLite → PostgreSQL**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres

# 2. Update .env
echo "DATABASE_URL=postgresql://finalytics_user:secure_password_change_me@localhost:5432/finalytics" > .env

# 3. Run migrations
alembic upgrade head

# 4. Done! Start your app
uvicorn app.main:app --reload
```

### **PostgreSQL → SQLite**
```bash
# 1. Update .env
echo "DATABASE_URL=sqlite:///./finalytics.db" > .env

# 2. Done! Start your app
uvicorn app.main:app --reload
```

---

## 📊 Database Operations

### **SQLite**
```bash
# View database
sqlite3 finalytics.db

# Show tables
.tables

# Show schema
.schema users

# Export data
.dump > backup.sql

# Query
SELECT * FROM users;
```

### **PostgreSQL**
```bash
# Connect
docker-compose exec postgres psql -U finalytics_user -d finalytics

# Or native
psql -U finalytics_user -d finalytics

# Show tables
\dt

# Show schema
\d+ users

# Export data
pg_dump -U finalytics_user finalytics > backup.sql

# Query
SELECT * FROM users;
```

---

## 🔧 Common Tasks

### **Reset Database**

#### SQLite
```bash
rm finalytics.db
alembic upgrade head
```

#### PostgreSQL
```bash
docker-compose exec postgres psql -U finalytics_user -d finalytics -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
alembic upgrade head
```

---

### **Backup Database**

#### SQLite
```bash
# Simple copy
cp finalytics.db backups/finalytics_$(date +%Y%m%d).db

# With .dump
sqlite3 finalytics.db .dump > backups/backup_$(date +%Y%m%d).sql
```

#### PostgreSQL
```bash
# Using pg_dump
docker-compose exec postgres pg_dump -U finalytics_user finalytics > backups/backup_$(date +%Y%m%d).sql

# Or compressed
docker-compose exec postgres pg_dump -U finalytics_user finalytics | gzip > backups/backup_$(date +%Y%m%d).sql.gz
```

---

### **Restore Database**

#### SQLite
```bash
# From backup file
cp backups/finalytics_20250129.db finalytics.db

# From .sql dump
sqlite3 finalytics.db < backups/backup_20250129.sql
```

#### PostgreSQL
```bash
# Drop and recreate
docker-compose exec postgres psql -U finalytics_user -d finalytics -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restore
docker-compose exec postgres psql -U finalytics_user finalytics < backups/backup_20250129.sql
```

---

## 🎯 Development Workflow

### **SQLite (Quick Start)**
```bash
# Clone repo
git clone <repo>
cd Finalytics

# Setup backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head

# Setup frontend
npm install

# Run (Terminal 1)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run (Terminal 2)
npm run dev

# Access
http://localhost:3000
```

### **PostgreSQL (Production-Like)**
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Update .env
DATABASE_URL=postgresql://finalytics_user:secure_password_change_me@localhost:5432/finalytics

# Run migrations
alembic upgrade head

# Run (Terminal 1)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Run (Terminal 2)
npm run dev

# Access
http://localhost:3000
```

---

## 🐛 Debugging

### **Check Database Connection**
```bash
# SQLite
python -c "from app.database import engine; print(engine.url)"

# PostgreSQL
docker-compose exec postgres pg_isready -U finalytics_user
```

### **View Logs**
```bash
# Docker PostgreSQL
docker-compose logs -f postgres

# FastAPI
uvicorn app.main:app --reload --log-level debug
```

### **Test Connection from Python**
```python
from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("✓ Database connected!")
```

---

## 📦 Docker Commands

### **PostgreSQL Management**
```bash
# Start
docker-compose up -d postgres

# Stop
docker-compose down

# Restart
docker-compose restart postgres

# View logs
docker-compose logs -f postgres

# Check status
docker-compose ps

# Remove (with data)
docker-compose down -v
```

### **pgAdmin (Web GUI)**
```bash
# Start pgAdmin
docker-compose --profile tools up -d pgadmin

# Access
http://localhost:5050
# Login: admin@finalytics.local / admin

# Stop
docker-compose --profile tools down
```

---

## 🔍 Health Checks

### **FastAPI Health**
```bash
curl http://localhost:8000/api/health
```

### **PostgreSQL Health**
```bash
docker-compose exec postgres pg_isready -U finalytics_user
```

### **Next.js Health**
```bash
curl http://localhost:3000
```

---

## 📈 Performance Monitoring

### **PostgreSQL Stats**
```sql
-- Connection count
SELECT count(*) FROM pg_stat_activity;

-- Active queries
SELECT pid, usename, query, state 
FROM pg_stat_activity 
WHERE state = 'active';

-- Table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### **Connection Pool (Python)**
```python
from app.database import engine

print(f"Pool size: {engine.pool.size()}")
print(f"Checked out: {engine.pool.checkedout()}")
print(f"Overflow: {engine.pool.overflow()}")
```

---

## 🆘 Emergency Commands

### **Kill All Connections (PostgreSQL)**
```sql
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'finalytics' AND pid <> pg_backend_pid();
```

### **Fix Stale Migrations**
```bash
# Mark all migrations as done (dangerous!)
alembic stamp head

# Or reset to specific revision
alembic stamp <revision_id>
```

### **Reset Everything**
```bash
# Nuclear option - delete everything and start fresh
rm -rf finalytics.db alembic/versions/*.py chroma_data/ storage/
docker-compose down -v
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

---

## 📞 Quick Help

| Issue | Command |
|-------|---------|
| Can't connect to PostgreSQL | `docker-compose up -d postgres` |
| Can't connect to SQLite | `ls -la finalytics.db` (check permissions) |
| Migration failed | `alembic downgrade -1 && alembic upgrade head` |
| Port 8000 in use | `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows) |
| Port 3000 in use | `lsof -i :3000` (macOS/Linux) or `netstat -ano | findstr :3000` (Windows) |
| Docker not working | `docker-compose restart` |

---

## 📚 Documentation Links

- **Migration Guide**: `MIGRATE_TO_POSTGRESQL.md`
- **Branch Comparison**: `BRANCH_COMPARISON.md`
- **Full Implementation**: `IMPLEMENTATION_SUMMARY.md`
- **Troubleshooting**: Check the guides above

---

**Print this card or keep it handy for quick reference!** 📋

