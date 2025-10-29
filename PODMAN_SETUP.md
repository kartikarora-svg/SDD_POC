# 🐋 Podman Setup Guide (Docker-Free)

This guide helps you run Finalytics using **Podman** instead of Docker.

---

## Why Podman?

| Feature | Docker | Podman |
|---------|--------|--------|
| **Daemon** | Requires background daemon | No daemon needed |
| **Root Access** | Needs admin/root | Can run rootless (more secure) |
| **Commands** | `docker`, `docker-compose` | `podman`, `podman-compose` |
| **Compatibility** | Standard | Docker-compatible |
| **License** | Free for personal use | Fully open source (Apache 2.0) |

---

## 📥 Installation

### Step 1: Install Podman Desktop

**You're already doing this!** ✅

1. Download: https://podman-desktop.io/downloads
2. Run installer
3. Complete the Podman machine setup (the dialog you're seeing)

**Settings for Podman Machine**:
- **Name**: `podman-machine-default` (keep default)
- **Image Path**: (leave empty or keep default)
- **Machine with root privileges**: **Enabled** ✅ (for PostgreSQL)
- **Start the machine now**: **Enabled** ✅

Click **Create** to finish!

---

### Step 2: Install podman-compose

**After Podman Desktop is installed**:

```bash
# Using pip (in your virtual environment)
pip install podman-compose

# Verify installation
podman-compose --version
```

**Expected output**: `podman-compose version 1.x.x`

---

## 🚀 Usage

### Start PostgreSQL with Podman

**Option 1: Using podman-compose (Easiest)**

```bash
# Navigate to project
cd C:\Users\kartik.arora\SDD\Finalytics

# Start PostgreSQL
podman-compose up -d postgres

# Check status
podman-compose ps

# View logs
podman-compose logs -f postgres

# Stop
podman-compose down
```

**Option 2: Using podman directly**

```bash
# Run PostgreSQL container
podman run -d \
  --name finalytics-postgres \
  -e POSTGRES_USER=finalytics_user \
  -e POSTGRES_PASSWORD=secure_password_change_me \
  -e POSTGRES_DB=finalytics \
  -p 5432:5432 \
  -v finalytics_pgdata:/var/lib/postgresql/data \
  postgres:16-alpine

# Check running containers
podman ps

# View logs
podman logs -f finalytics-postgres

# Stop container
podman stop finalytics-postgres

# Remove container
podman rm finalytics-postgres
```

---

## 📋 Complete Workflow

### 1. Start Podman Machine

```bash
# Check if machine is running
podman machine list

# If not running, start it
podman machine start podman-machine-default
```

**Expected output**:
```
Starting machine "podman-machine-default"
Machine "podman-machine-default" is now running
```

---

### 2. Start PostgreSQL

```bash
# Use existing docker-compose.yml with Podman
podman-compose up -d postgres
```

**Expected output**:
```
Creating network finalytics_default
Creating volume finalytics_postgres_data
Creating finalytics-postgres ... done
```

---

### 3. Configure Finalytics

**Update `.env`** (same as before):
```bash
DATABASE_URL=postgresql://finalytics_user:secure_password_change_me@localhost:5432/finalytics
```

---

### 4. Run Migrations

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run migrations
alembic upgrade head
```

---

### 5. Start Application

```bash
# Terminal 1: FastAPI Backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Next.js Frontend
npm run dev
```

**Access**: http://localhost:3000

---

## 🔧 Podman Commands Reference

### Container Management

```bash
# List running containers
podman ps

# List all containers (including stopped)
podman ps -a

# Start container
podman start <container_name>

# Stop container
podman stop <container_name>

# Remove container
podman rm <container_name>

# View logs
podman logs -f <container_name>

# Execute command in container
podman exec -it <container_name> psql -U finalytics_user -d finalytics
```

---

### Volume Management

```bash
# List volumes
podman volume ls

# Inspect volume
podman volume inspect finalytics_postgres_data

# Remove volume (WARNING: deletes data!)
podman volume rm finalytics_postgres_data
```

---

### Machine Management

```bash
# List machines
podman machine list

# Start machine
podman machine start podman-machine-default

# Stop machine
podman machine stop podman-machine-default

# SSH into machine
podman machine ssh podman-machine-default

# Check machine status
podman machine inspect podman-machine-default
```

---

## 🔄 Migration from Docker to Podman

If you were previously using Docker:

### Step 1: Stop Docker Containers

```bash
docker-compose down
```

### Step 2: Create Podman Machine

Already done! (The dialog you're seeing)

### Step 3: Use podman-compose

```bash
# Same docker-compose.yml file works!
podman-compose up -d
```

**That's it!** Your existing `docker-compose.yml` is compatible.

---

## 🛠️ Troubleshooting

### Issue: "podman-compose: command not found"

**Solution**:
```bash
pip install podman-compose
```

### Issue: "Error: cannot find podman"

**Solution**: Add Podman to PATH or restart terminal after installation.

**Windows**: Restart Podman Desktop or terminal.

---

### Issue: "no podman machine is running"

**Solution**:
```bash
# Start the machine
podman machine start podman-machine-default

# Or create a new one
podman machine init
podman machine start
```

---

### Issue: Port 5432 already in use

**Solution**: Stop native PostgreSQL or Docker PostgreSQL first.

```bash
# Stop native PostgreSQL
net stop postgresql-x64-16

# Or stop Docker PostgreSQL
docker-compose down
```

---

### Issue: "Error: short-name resolution enforced"

**Solution**: Use full image name:
```bash
# Instead of: postgres:16-alpine
# Use: docker.io/library/postgres:16-alpine
```

Or add to `/etc/containers/registries.conf`:
```toml
unqualified-search-registries = ["docker.io"]
```

---

## ⚙️ Configuration Files

### Your Existing docker-compose.yml Works!

Podman uses the same `docker-compose.yml` format. No changes needed!

**File**: `docker-compose.yml` (already exists)
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: finalytics-postgres
    environment:
      POSTGRES_USER: finalytics_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure_password_change_me}
      POSTGRES_DB: finalytics
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## 🎯 Quick Start Script

Create `start-podman.sh` (or `.bat` for Windows):

**PowerShell** (`start-podman.ps1`):
```powershell
# Start Podman machine if not running
$machine = podman machine list --format json | ConvertFrom-Json
if ($machine.Running -ne $true) {
    Write-Host "Starting Podman machine..."
    podman machine start podman-machine-default
    Start-Sleep -Seconds 5
}

# Start PostgreSQL
Write-Host "Starting PostgreSQL..."
podman-compose up -d postgres

# Wait for PostgreSQL to be ready
Write-Host "Waiting for PostgreSQL..."
Start-Sleep -Seconds 5

# Check status
podman-compose ps

Write-Host "`n✓ PostgreSQL is running!"
Write-Host "Connect with: psql -U finalytics_user -d finalytics -h localhost"
```

**Usage**:
```powershell
.\start-podman.ps1
```

---

## 📊 Podman Desktop GUI

### What You Can Do:

1. **View Containers**: See running PostgreSQL container
2. **View Logs**: Real-time log streaming
3. **Manage Volumes**: View and delete data volumes
4. **Port Mapping**: See which ports are exposed
5. **Resource Usage**: Monitor CPU/memory usage

### Quick Actions:

- **Start/Stop containers**: Click the play/stop button
- **Delete containers**: Right-click → Delete
- **View logs**: Click container → Logs tab
- **Open terminal**: Click container → Terminal tab

---

## 🔐 Security Benefits

### Rootless Mode

Podman runs containers without root privileges by default:

```bash
# Check if running rootless
podman info | grep rootless
# Should show: rootless: true
```

**Benefits**:
- ✅ More secure (no root daemon)
- ✅ Better isolation
- ✅ No privilege escalation risks

---

## 🎓 Learning Resources

- **Podman Docs**: https://docs.podman.io/
- **Podman Desktop**: https://podman-desktop.io/docs
- **Migrate from Docker**: https://docs.podman.io/en/latest/markdown/podman-compose.1.html

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Podman machine is running (`podman machine list`)
- [ ] PostgreSQL container is running (`podman ps`)
- [ ] Can connect to PostgreSQL (`psql -U finalytics_user -d finalytics -h localhost`)
- [ ] FastAPI connects to database (check startup logs)
- [ ] Can register/login in the app
- [ ] Data persists after restart

---

## 🎉 Summary

**You're now running Podman instead of Docker!**

**Key Commands**:
```bash
# Start everything
podman machine start podman-machine-default
podman-compose up -d postgres

# Stop everything
podman-compose down
podman machine stop podman-machine-default

# Check status
podman machine list
podman ps
```

**That's it! No Docker needed.** 🚀

