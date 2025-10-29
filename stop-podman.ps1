# Stop Podman Services for Finalytics
# Usage: .\stop-podman.ps1

Write-Host "🛑 Stopping Finalytics Podman services..." -ForegroundColor Cyan
Write-Host ""

# Stop containers
Write-Host "Stopping PostgreSQL..." -ForegroundColor Cyan
podman-compose -f podman-compose.yml down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL stopped" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to stop PostgreSQL" -ForegroundColor Red
}

Write-Host ""

# Ask if user wants to stop Podman machine
$response = Read-Host "Do you want to stop the Podman machine? (y/N)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "Stopping Podman machine..." -ForegroundColor Cyan
    podman machine stop
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Podman machine stopped" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to stop Podman machine" -ForegroundColor Red
    }
} else {
    Write-Host "Keeping Podman machine running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Done!" -ForegroundColor Green

