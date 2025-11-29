# Quick run script for Veritas Guardian
# Choose which component to run

param(
    [Parameter(Position=0)]
    [ValidateSet('ui', 'api', 'test', 'help')]
    [string]$Command = 'help'
)

$ErrorActionPreference = "Stop"

function Show-Help {
    Write-Host ""
    Write-Host "🛡️  VERITAS GUARDIAN - Run Script" -ForegroundColor Cyan
    Write-Host "=" -NoNewline; Write-Host ("=" * 79)
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 ui       " -NoNewline -ForegroundColor Green
    Write-Host "Start Streamlit UI (recommended)"
    Write-Host "  .\run.ps1 api      " -NoNewline -ForegroundColor Green
    Write-Host "Start FastAPI backend"
    Write-Host "  .\run.ps1 test     " -NoNewline -ForegroundColor Green
    Write-Host "Run system tests"
    Write-Host "  .\run.ps1 help     " -NoNewline -ForegroundColor Green
    Write-Host "Show this help"
    Write-Host ""
}

function Check-VirtualEnv {
    if (-not (Test-Path ".venv")) {
        Write-Host "❌ Virtual environment not found" -ForegroundColor Red
        Write-Host "   Run setup.ps1 first" -ForegroundColor Yellow
        exit 1
    }
}

function Check-EnvFile {
    if (-not (Test-Path ".env")) {
        Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
        Write-Host "   Creating from .env.example..." -ForegroundColor Cyan
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file" -ForegroundColor Green
        Write-Host "   IMPORTANT: Edit .env and add your GEMINI_API_KEY" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter when you've configured .env"
    }
}

function Activate-VirtualEnv {
    Write-Host "🔌 Activating virtual environment..." -ForegroundColor Cyan
    & .\.venv\Scripts\Activate.ps1
}

function Start-StreamlitUI {
    Write-Host ""
    Write-Host "🎨 Starting Streamlit UI..." -ForegroundColor Cyan
    Write-Host "   URL: http://localhost:8501" -ForegroundColor Green
    Write-Host ""
    streamlit run app.py
}

function Start-FastAPI {
    Write-Host ""
    Write-Host "🚀 Starting FastAPI backend..." -ForegroundColor Cyan
    Write-Host "   API: http://localhost:8000" -ForegroundColor Green
    Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor Green
    Write-Host ""
    uvicorn backend:app --reload --port 8000
}

function Run-Tests {
    Write-Host ""
    Write-Host "🧪 Running system tests..." -ForegroundColor Cyan
    Write-Host ""
    python scripts/test_system.py
}

# Main logic
switch ($Command) {
    'ui' {
        Check-VirtualEnv
        Check-EnvFile
        Activate-VirtualEnv
        Start-StreamlitUI
    }
    'api' {
        Check-VirtualEnv
        Check-EnvFile
        Activate-VirtualEnv
        Start-FastAPI
    }
    'test' {
        Check-VirtualEnv
        Activate-VirtualEnv
        Run-Tests
    }
    'help' {
        Show-Help
    }
}
