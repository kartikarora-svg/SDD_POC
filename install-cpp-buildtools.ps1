# Install Microsoft C++ Build Tools for Python packages
# This script helps install the required build tools

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Microsoft C++ Build Tools Installation"  -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "ChromaDB requires Visual C++ 14.0+ to compile native extensions.`n"

Write-Host "Installation Options:`n" -ForegroundColor Yellow

Write-Host "Option 1: Install via winget (Quickest)" -ForegroundColor Green
Write-Host "  Command: winget install Microsoft.VisualStudio.2022.BuildTools`n"

Write-Host "Option 2: Download installer manually" -ForegroundColor Green  
Write-Host "  URL: https://visualstudio.microsoft.com/visual-cpp-build-tools/`n"

Write-Host "What components to install:" -ForegroundColor Yellow
Write-Host "  ✓ Desktop development with C++" -ForegroundColor White
Write-Host "  ✓ MSVC v143 - VS 2022 C++ x64/x86 build tools" -ForegroundColor White
Write-Host "  ✓ Windows SDK (latest version)`n" -ForegroundColor White

$choice = Read-Host "Install now using winget? (Y/N)"

if ($choice -eq 'Y' -or $choice -eq 'y') {
    Write-Host "`nInstalling Visual Studio Build Tools..." -ForegroundColor Green
    winget install Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Build Tools installed successfully!" -ForegroundColor Green
        Write-Host "`nNext steps:" -ForegroundColor Yellow
        Write-Host "1. Close this terminal" -ForegroundColor White
        Write-Host "2. Open a NEW terminal" -ForegroundColor White
        Write-Host "3. Activate your virtual environment: .venv\Scripts\activate" -ForegroundColor White
        Write-Host "4. Run: pip install -r requirements-py313.txt`n" -ForegroundColor White
    } else {
        Write-Host "`n✗ Installation failed. Try manual installation.`n" -ForegroundColor Red
        Write-Host "Manual installation URL:" -ForegroundColor Yellow
        Write-Host "https://visualstudio.microsoft.com/visual-cpp-build-tools/`n" -ForegroundColor Cyan
    }
} else {
    Write-Host "`nManual installation:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor White
    Write-Host "2. Download 'Build Tools for Visual Studio 2022'" -ForegroundColor White
    Write-Host "3. Run installer" -ForegroundColor White
    Write-Host "4. Select 'Desktop development with C++'" -ForegroundColor White
    Write-Host "5. Click Install`n" -ForegroundColor White
    
    $openBrowser = Read-Host "Open download page in browser? (Y/N)"
    if ($openBrowser -eq 'Y' -or $openBrowser -eq 'y') {
        Start-Process "https://visualstudio.microsoft.com/visual-cpp-build-tools/"
    }
}

