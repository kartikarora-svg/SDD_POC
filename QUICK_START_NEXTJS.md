# 🚀 Quick Start - Next.js Version

## Current Status
✅ **Authentication pages are complete and working!**
- Login page fully functional
- Register page fully functional  
- JWT authentication integrated
- Navigation shows user state

## Test It Now!

### Step 1: Ensure You're on the Right Branch
```powershell
git checkout feature/nextjs-frontend
git branch  # Should show * feature/nextjs-frontend
```

### Step 2: Start FastAPI Backend  
```powershell
# Terminal 1
cd C:\Users\kartik.arora\SDD\Finalytics
.venv\Scripts\activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Wait for**: `INFO: Application startup complete`

### Step 3: Start Next.js Frontend
```powershell
# Terminal 2 (NEW terminal)
cd C:\Users\kartik.arora\SDD\Finalytics
cmd /c "npm run dev"
```

**Wait for**: `Ready on http://localhost:3000`

### Step 4: Open Browser
Go to: **http://localhost:3000**

You should see:
- ✅ Finalytics home page with 4 feature cards
- ✅ Navigation bar with Login link
- ✅ Responsive design

### Step 5: Test Authentication
1. Click **"Login"** in navigation
2. Click **"Register"** to create an account
3. Enter email and password
4. Click **"Create Account"**
5. You'll be auto-logged in and redirected
6. Navigation will show **"Welcome, your@email.com"** and **"Logout"**

---

## 📊 What's Working vs What's Pending

### ✅ Complete
- Home page
- Login page
- Register page
- Navigation (with auth state)
- Footer
- API integration
- JWT authentication
- Routing

### ⏳ To Be Migrated
- Documents page (upload, Q&A)
- News feed (scraping, summaries)
- Stock intelligence (queries)
- Stock comparison (side-by-side)

---

## 🔄 Switch Back to Vanilla Version

If you want to test the original vanilla JS version:

```powershell
# Stop Next.js dev server (Ctrl+C in Terminal 2)
# Keep FastAPI running

# Switch branch
git checkout master

# Open browser
http://localhost:8000
```

All features work in the vanilla version!

---

## 🐛 Troubleshooting

### Problem: `npm run dev` fails with script execution policy
**Solution**: Use `cmd /c "npm run dev"` instead

### Problem: Port 3000 already in use
**Solution**: 
```powershell
# Find process
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess

# Kill it
Stop-Process -Id [PID]
```

### Problem: Backend API not responding
**Solution**: Make sure FastAPI is running on port 8000 first

### Problem: Login doesn't work
**Solution**: 
1. Check FastAPI terminal for errors
2. Check browser console (F12) for network errors
3. Ensure you registered an account first

---

## 📝 Next Steps

You have 3 options:

### Option 1: Continue Migration Yourself
Use the existing structure as a template:
- Copy patterns from `app/login/page.tsx`
- Use `apiCall()` from `lib/api.ts`
- Refer to original JS files in `static/js/`

### Option 2: Ask Me to Continue
I can finish migrating the remaining 4 pages:
- Documents
- News
- Stocks  
- Compare

### Option 3: Use Both Versions
- Use Next.js for production (better performance)
- Keep vanilla JS for quick testing
- Switch between them as needed

---

## 📞 Key Commands

| Action | Command |
|--------|---------|
| Check current branch | `git branch` |
| Switch to Next.js | `git checkout feature/nextjs-frontend` |
| Switch to vanilla | `git checkout master` |
| Start backend | `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload` |
| Start Next.js | `cmd /c "npm run dev"` |
| View logs | Check both terminal windows |

---

**Ready to test? Start both servers and visit http://localhost:3000!** 🎉

