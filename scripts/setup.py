"""
Setup script to initialize Veritas Guardian environment
"""

import os
import subprocess
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    dirs = ['temp', 'receipts', 'data', 'logs', 'temp/uploads']
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_env_file():
    """Check for .env file"""
    if not Path('.env').exists():
        print("⚠️  .env file not found. Please create one from .env.example")
        print("   Copy .env.example to .env and add your GEMINI_API_KEY")
        return False
    print("✅ .env file found")
    return True

def check_system_dependencies():
    """Check for system binaries"""
    print("\n🔍 Checking system dependencies...")
    
    # Check FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        print("✅ FFmpeg installed")
    except:
        print("❌ FFmpeg not found. Please install:")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
    
    # Check Tesseract
    try:
        subprocess.run(['tesseract', '--version'], 
                      capture_output=True, check=True)
        print("✅ Tesseract OCR installed")
    except:
        print("❌ Tesseract not found. Please install:")
        print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   macOS: brew install tesseract")
        print("   Linux: sudo apt install tesseract-ocr")

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python packages...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True)
        print("✅ Requirements installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def download_whisper_model():
    """Download Whisper tiny model"""
    print("\n🎤 Downloading Whisper model (this may take a moment)...")
    try:
        import whisper
        whisper.load_model("tiny")
        print("✅ Whisper model ready")
    except Exception as e:
        print(f"⚠️  Whisper model download deferred: {e}")

def main():
    print("=" * 80)
    print("🛡️  VERITAS GUARDIAN - Setup")
    print("=" * 80)
    
    # Check Python
    check_python_version()
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Check .env
    print("\n🔑 Checking environment...")
    env_ok = check_env_file()
    
    # Check system dependencies
    check_system_dependencies()
    
    # Install requirements
    install_requirements()
    
    # Download models
    download_whisper_model()
    
    print("\n" + "=" * 80)
    if env_ok:
        print("✅ Setup complete! You can now run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Setup complete, but please configure .env file first!")
    print("=" * 80)

if __name__ == "__main__":
    main()
