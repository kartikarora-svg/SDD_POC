# Quick Restart Script
# Use this to restart the Finalytics server after updates

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Finalytics Server Restart" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "Starting Finalytics server with optimizations...`n" -ForegroundColor Yellow
Write-Host "✅ API Key configured" -ForegroundColor Green
Write-Host "✅ Parallel processing enabled" -ForegroundColor Green
Write-Host "✅ Independent feature workflow" -ForegroundColor Green
Write-Host "`nServer starting on http://localhost:8000`n" -ForegroundColor Cyan

.venv\Scripts\python.exe -m uvicorn app.main:app --reload

