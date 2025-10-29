# 🚀 Podman Quick Start

**You're on the right track with that Podman machine dialog!**

---

## ✅ What Was Added

4 new files to support Podman (Docker-free):

1. **PODMAN_SETUP.md** - Complete guide (troubleshooting, commands, etc.)
2. **podman-compose.yml** - Podman-optimized compose file
3. **start-podman.ps1** - Automated startup script
4. **stop-podman.ps1** - Automated shutdown script

---

## 🎯 Next Steps (After Creating Podman Machine)

### Step 1: Finish Creating Podman Machine

**In the dialog you're seeing**:
- ✅ Keep "Machine with root privileges" **Enabled**
- ✅ Keep "Start the machine now" **Enabled**
- Click **"Create"** button

Wait 30-60 seconds for the machine to be created.

---

### Step 2: Install podman-compose

```bash
# In your virtual environment
pip install podman-compose
```

---

### Step 3: Choose Your Method

#### **Option A: Automated (Easiest)**

```powershell
# Just run this script!
.\start-podman.ps1
```

**This script automatically**:
- ✅ Checks if Podman is installed
- ✅ Starts Podman machine
- ✅ Starts PostgreSQL
- ✅ Waits for database to be ready
- ✅ Shows you what to do next

---

#### **Option B: Manual**

```bash
# 1. Verify machine is running
podman machine list

# 2. Start PostgreSQL
podman-compose -f podman-compose.yml up -d postgres

# 3. Check status
podman ps
```

---

### Step 4: Update .env

```bash
DATABASE_URL=postgresql://finalytics_user:secure_password_change_me@localhost:5432/finalytics
```

---

### Step 5: Run Migrations

```bash
alembic upgrade head
```

---

### Step 6: Start Application

```bash
# Terminal 1: FastAPI
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Next.js
npm run dev
```

**Access**: http://localhost:3000

---

## 📊 Summary

| What | Command |
|------|---------|
| **Start everything** | `.\start-podman.ps1` |
| **Stop everything** | `.\stop-podman.ps1` |
| **Check status** | `podman ps` |
| **View logs** | `podman-compose logs -f` |
| **Stop services** | `podman-compose down` |

---

## 🆘 If Something Goes Wrong

### "Podman machine not running"

```bash
podman machine start podman-machine-default
```

### "Port 5432 already in use"

Stop native PostgreSQL first:
```bash
net stop postgresql-x64-16
```

---

## 📖 Full Documentation

See **PODMAN_SETUP.md** for:
- Complete troubleshooting guide
- All Podman commands
- Security features
- Migration from Docker

---

**Ready?** Finish creating your Podman machine in that dialog, then run `.\start-podman.ps1`! 🎉

