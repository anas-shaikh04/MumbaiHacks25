"""
Pre-flight check for Veritas Guardian
Verifies all dependencies and configuration before running
"""

import sys
import os
import subprocess
from pathlib import Path

# Color codes for terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print("=" * 80)

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} found (need 3.9+)")
        return False

def check_virtual_env():
    """Check if virtual environment exists and is activated"""
    venv_path = Path(".venv")
    if venv_path.exists():
        print_success("Virtual environment found")
        
        # Check if activated
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print_success("Virtual environment is activated")
            return True
        else:
            print_warning("Virtual environment not activated")
            print_info("Run: .venv\\Scripts\\Activate.ps1")
            return False
    else:
        print_error("Virtual environment not found")
        print_info("Run: python -m venv .venv")
        return False

def check_env_file():
    """Check .env file and API key"""
    env_path = Path(".env")
    if not env_path.exists():
        print_error(".env file not found")
        print_info("Run: Copy-Item .env.example .env")
        return False
    
    print_success(".env file exists")
    
    # Check API key
    with open(env_path, 'r') as f:
        content = f.read()
        if "GEMINI_API_KEY=" in content:
            if "your_gemini_api_key_here" in content or "GEMINI_API_KEY=\n" in content:
                print_warning("GEMINI_API_KEY not configured")
                print_info("Edit .env and add your API key from https://ai.google.dev/")
                return False
            else:
                print_success("GEMINI_API_KEY configured")
                return True
    
    print_error("GEMINI_API_KEY not found in .env")
    return False

def check_system_binary(name, command, install_info):
    """Check if system binary is installed"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            shell=True,
            timeout=5
        )
        if result.returncode == 0:
            print_success(f"{name} installed")
            return True
        else:
            print_error(f"{name} not found")
            print_info(install_info)
            return False
    except Exception as e:
        print_error(f"{name} not found")
        print_info(install_info)
        return False

def check_directories():
    """Check required directories"""
    required_dirs = ['temp', 'receipts', 'data', 'logs', 'temp/uploads']
    all_exist = True
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print_success(f"Directory '{dir_name}' exists")
        else:
            print_warning(f"Directory '{dir_name}' missing")
            dir_path.mkdir(parents=True, exist_ok=True)
            print_info(f"Created '{dir_name}'")
    
    return True

def check_credibility_db():
    """Check credibility database"""
    db_path = Path("data/credibility.csv")
    if db_path.exists():
        # Count entries
        with open(db_path, 'r') as f:
            lines = len(f.readlines()) - 1  # Exclude header
        print_success(f"Credibility database exists ({lines} sources)")
        return True
    else:
        print_warning("Credibility database not found")
        print_info("Run: python scripts/init_credibility_db.py")
        return False

def check_python_packages():
    """Check critical Python packages"""
    packages = [
        ('streamlit', 'streamlit'),
        ('fastapi', 'fastapi'),
        ('whisper', 'openai-whisper'),
        ('google.generativeai', 'google-generativeai'),
        ('PIL', 'Pillow'),
        ('duckduckgo_search', 'duckduckgo-search'),
    ]
    
    all_installed = True
    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print_success(f"Package '{package_name}' installed")
        except ImportError:
            print_error(f"Package '{package_name}' not found")
            print_info(f"Run: pip install {package_name}")
            all_installed = False
    
    return all_installed

def main():
    print_header("🛡️  VERITAS GUARDIAN - Pre-flight Check")
    
    checks = {
        "Python Version": check_python_version(),
        "Virtual Environment": check_virtual_env(),
        "Environment File": check_env_file(),
        "FFmpeg": check_system_binary(
            "FFmpeg",
            "ffmpeg -version",
            "Download from https://ffmpeg.org/download.html"
        ),
        "Tesseract": check_system_binary(
            "Tesseract",
            "tesseract --version",
            "Download from https://github.com/UB-Mannheim/tesseract/wiki"
        ),
        "Directories": check_directories(),
        "Credibility Database": check_credibility_db(),
        "Python Packages": check_python_packages()
    }
    
    print_header("📊 Summary")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for check_name, result in checks.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{check_name:25s} {status}")
    
    print(f"\n{Colors.BOLD}Score: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All checks passed! System is ready to run.{Colors.END}")
        print(f"\n{Colors.CYAN}Run the application:{Colors.END}")
        print(f"  {Colors.YELLOW}streamlit run app.py{Colors.END}")
        print(f"  {Colors.YELLOW}uvicorn backend:app --reload{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  Some checks failed. Please fix issues above.{Colors.END}")
        print(f"\n{Colors.CYAN}Quick fixes:{Colors.END}")
        print(f"  {Colors.YELLOW}pip install -r requirements.txt{Colors.END}")
        print(f"  {Colors.YELLOW}python scripts/init_credibility_db.py{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
