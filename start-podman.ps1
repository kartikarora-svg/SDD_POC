# Start Podman Machine and PostgreSQL for Finalytics
# Usage: .\start-podman.ps1

Write-Host "🚀 Starting Finalytics with Podman..." -ForegroundColor Cyan
Write-Host ""

# Check if Podman is installed
try {
    $podmanVersion = podman --version
    Write-Host "✓ Podman found: $podmanVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Podman not found! Please install Podman Desktop first." -ForegroundColor Red
    Write-Host "  Download: https://podman-desktop.io/downloads" -ForegroundColor Yellow
    exit 1
}

# Check if podman-compose is installed
try {
    $composeVersion = podman-compose --version
    Write-Host "✓ podman-compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ podman-compose not found! Installing..." -ForegroundColor Yellow
    pip install podman-compose
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install podman-compose" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ podman-compose installed" -ForegroundColor Green
}

Write-Host ""

# Check if Podman machine exists
Write-Host "Checking Podman machine status..." -ForegroundColor Cyan
$machineList = podman machine list --format json | ConvertFrom-Json

if (-not $machineList) {
    Write-Host "✗ No Podman machine found. Creating one..." -ForegroundColor Yellow
    podman machine init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to create Podman machine" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Podman machine created" -ForegroundColor Green
}

# Start Podman machine if not running
$machine = $machineList | Select-Object -First 1
if ($machine.Running -ne $true) {
    Write-Host "Starting Podman machine: $($machine.Name)..." -ForegroundColor Cyan
    podman machine start $machine.Name
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to start Podman machine" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Podman machine started" -ForegroundColor Green
    Start-Sleep -Seconds 3
} else {
    Write-Host "✓ Podman machine is already running" -ForegroundColor Green
}

Write-Host ""

# Start PostgreSQL using podman-compose
Write-Host "Starting PostgreSQL with podman-compose..." -ForegroundColor Cyan
podman-compose -f podman-compose.yml up -d postgres

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start PostgreSQL" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Wait for PostgreSQL to be ready
Write-Host "Waiting for PostgreSQL to be ready..." -ForegroundColor Cyan
$maxRetries = 30
$retries = 0

while ($retries -lt $maxRetries) {
    $health = podman exec finalytics-postgres pg_isready -U finalytics_user 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PostgreSQL is ready!" -ForegroundColor Green
        break
    }
    $retries++
    Write-Host "  Waiting... ($retries/$maxRetries)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
}

if ($retries -eq $maxRetries) {
    Write-Host "✗ PostgreSQL failed to start in time" -ForegroundColor Red
    Write-Host "  Check logs with: podman-compose logs postgres" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Show status
Write-Host "📊 Container Status:" -ForegroundColor Cyan
podman-compose ps

Write-Host ""
Write-Host "✅ Finalytics Podman setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Update .env file:" -ForegroundColor White
Write-Host "     DATABASE_URL=postgresql://finalytics_user:secure_password_change_me@localhost:5432/finalytics" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Run migrations:" -ForegroundColor White
Write-Host "     alembic upgrade head" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Start FastAPI (Terminal 1):" -ForegroundColor White
Write-Host "     uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. Start Next.js (Terminal 2):" -ForegroundColor White
Write-Host "     npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "  5. Access: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  podman-compose logs -f postgres   # View logs" -ForegroundColor Gray
Write-Host "  podman-compose down               # Stop services" -ForegroundColor Gray
Write-Host "  podman ps                         # List containers" -ForegroundColor Gray

