# Windows Setup Script for Veritas Guardian
# Run this script in PowerShell to set up the environment

Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 79) -ForegroundColor Blue
Write-Host "🛡️  VERITAS GUARDIAN - Windows Setup" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 79) -ForegroundColor Blue
Write-Host ""

# Check Python
Write-Host "🐍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "   ℹ️  Virtual environment already exists" -ForegroundColor Cyan
} else {
    python -m venv .venv
    Write-Host "   ✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "   ✅ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "   ✅ pip upgraded" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "📚 Installing Python packages..." -ForegroundColor Yellow
Write-Host "   (This may take several minutes...)" -ForegroundColor Cyan
python -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ All packages installed" -ForegroundColor Green
} else {
    Write-Host "   ❌ Package installation failed" -ForegroundColor Red
    exit 1
}

# Create directories
Write-Host ""
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
$dirs = @("temp", "receipts", "data", "logs", "temp/uploads")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
Write-Host "   ✅ Directories created" -ForegroundColor Green

# Check .env file
Write-Host ""
Write-Host "🔑 Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  .env file not found" -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "   ✅ Created .env from .env.example" -ForegroundColor Green
        Write-Host "   ⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY" -ForegroundColor Yellow
    } else {
        Write-Host "   ❌ .env.example not found" -ForegroundColor Red
    }
}

# Initialize credibility database
Write-Host ""
Write-Host "🗃️  Initializing credibility database..." -ForegroundColor Yellow
python scripts/init_credibility_db.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Credibility database initialized" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Database initialization had issues" -ForegroundColor Yellow
}

# Check system dependencies
Write-Host ""
Write-Host "🔍 Checking system dependencies..." -ForegroundColor Yellow

# Check FFmpeg
Write-Host "   Checking FFmpeg..." -ForegroundColor Cyan
try {
    ffmpeg -version 2>&1 | Out-Null
    Write-Host "   ✅ FFmpeg installed" -ForegroundColor Green
} catch {
    Write-Host "   ❌ FFmpeg not found" -ForegroundColor Red
    Write-Host "      Download from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    Write-Host "      Extract and add to PATH" -ForegroundColor Yellow
}

# Check Tesseract
Write-Host "   Checking Tesseract OCR..." -ForegroundColor Cyan
try {
    tesseract --version 2>&1 | Out-Null
    Write-Host "   ✅ Tesseract installed" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Tesseract not found" -ForegroundColor Red
    Write-Host "      Download from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    Write-Host "      Install and add to PATH" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 79) -ForegroundColor Blue
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Make sure FFmpeg and Tesseract are installed" -ForegroundColor White
Write-Host "  2. Edit .env and add your GEMINI_API_KEY" -ForegroundColor White
Write-Host "  3. Run the application:" -ForegroundColor White
Write-Host "     streamlit run app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "For API server:" -ForegroundColor Cyan
Write-Host "     uvicorn backend:app --reload" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 79) -ForegroundColor Blue
