# Quick Start Script for Veritas Guardian React Frontend

Write-Host "🛡️ Veritas Guardian - React Frontend Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check if npm is installed
Write-Host "Checking npm installation..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm is not installed. Please install Node.js which includes npm." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
Write-Host ""

Set-Location frontend

# Install dependencies
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Setup complete! You can now:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Start the backend:" -ForegroundColor White
    Write-Host "   python backend.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Start the frontend (in a new terminal):" -ForegroundColor White
    Write-Host "   cd frontend" -ForegroundColor Gray
    Write-Host "   npm run dev" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Access the app:" -ForegroundColor White
    Write-Host "   Main page: http://localhost:5173" -ForegroundColor Gray
    Write-Host "   Verification: http://localhost:5173/verify" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📖 For more information, see:" -ForegroundColor Yellow
    Write-Host "   - frontend/FRONTEND_GUIDE.md" -ForegroundColor Gray
    Write-Host "   - MIGRATION_SUMMARY.md" -ForegroundColor Gray
    Write-Host ""
    
    # Ask if user wants to start dev server
    $startServer = Read-Host "Would you like to start the development server now? (y/n)"
    if ($startServer -eq "y" -or $startServer -eq "Y") {
        Write-Host ""
        Write-Host "🚀 Starting frontend development server..." -ForegroundColor Cyan
        Write-Host "📌 Make sure the backend is running on http://localhost:8000" -ForegroundColor Yellow
        Write-Host ""
        npm run dev
    }
} else {
    Write-Host ""
    Write-Host "❌ Failed to install dependencies. Please check the error messages above." -ForegroundColor Red
    Write-Host ""
}

Set-Location ..
