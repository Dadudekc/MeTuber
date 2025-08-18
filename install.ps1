# MeTuber Installation Script for Windows
# Run this script in PowerShell as Administrator for best results

param(
    [switch]$Core,
    [switch]$Full,
    [switch]$Dev,
    [switch]$SkipDeps,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
MeTuber Installation Script

Usage:
    .\install.ps1 [options]

Options:
    -Core        Install only core dependencies (minimal)
    -Full        Install all dependencies including optional features
    -Dev         Install development dependencies
    -SkipDeps    Skip dependency installation (for development)
    -Help        Show this help message

Examples:
    .\install.ps1 -Core          # Install minimal dependencies
    .\install.ps1 -Full          # Install all dependencies
    .\install.ps1 -Dev           # Install development dependencies
    .\install.ps1 -SkipDeps      # Skip dependency installation

"@
    exit 0
}

Write-Host "MeTuber Installation Script" -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please ensure pip is installed with Python." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists. Removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}

# Create virtual environment
Write-Host "🔧 Creating virtual environment..." -ForegroundColor Blue
python -m venv venv

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "🔧 Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip

# Install dependencies based on flags
if (-not $SkipDeps) {
    if ($Core) {
        Write-Host "📦 Installing core dependencies..." -ForegroundColor Blue
        pip install -r requirements-core.txt
    } elseif ($Full) {
        Write-Host "📦 Installing all dependencies..." -ForegroundColor Blue
        pip install -r requirements.txt
    } elseif ($Dev) {
        Write-Host "📦 Installing development dependencies..." -ForegroundColor Blue
        pip install -r requirements.txt
        pip install -e .[dev]
    } else {
        # Default: install core dependencies
        Write-Host "📦 Installing core dependencies..." -ForegroundColor Blue
        pip install -r requirements-core.txt
    }
}

# Check dependencies
Write-Host "🔍 Checking dependencies..." -ForegroundColor Blue
python check_dependencies.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run MeTuber:" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  python webcam_filter_pyqt5.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use the shortcut:" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\metuber.exe" -ForegroundColor White
} else {
    Write-Host "❌ Installation completed with warnings. Check the output above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Note: You may need to install OBS Studio for virtual camera support." -ForegroundColor Cyan
Write-Host "Download from: https://obsproject.com/" -ForegroundColor Cyan


