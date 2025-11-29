# Veritas Guardian - Quick Start Guide

## 🚀 Quick Setup (Windows)

### 1. Run Setup Script
```powershell
# Run in PowerShell
.\setup.ps1
```

This will:
- Create virtual environment
- Install all Python packages
- Create necessary directories
- Initialize credibility database

### 2. Configure API Key

Edit `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_key_here
```

Get your key from: https://ai.google.dev/

### 3. Install System Dependencies

**FFmpeg** (required for video/audio):
- Download: https://ffmpeg.org/download.html
- Extract and add to PATH

**Tesseract OCR** (required for image text):
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Install and add to PATH

### 4. Run the Application

**Streamlit UI (Recommended for demo):**
```powershell
streamlit run app.py
```

**FastAPI Backend:**
```powershell
uvicorn backend:app --reload --port 8000
```

## 📚 Manual Setup

If the script doesn't work, follow these steps:

### Create Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install Requirements
```powershell
pip install -r requirements.txt
```

### Create Directories
```powershell
New-Item -ItemType Directory -Force -Path temp, receipts, data, logs, temp/uploads
```

### Initialize Database
```powershell
python scripts/init_credibility_db.py
```

### Configure Environment
```powershell
Copy-Item .env.example .env
# Edit .env with your API keys
```

## 🧪 Testing

Test with a simple claim:
```python
python pipeline.py
```

## 📖 Usage Examples

### Text Verification
1. Open Streamlit UI
2. Go to "Text" tab
3. Paste: "5G towers cause COVID-19"
4. Click "Verify Text"
5. View results with evidence and risk analysis

### Image Verification
1. Go to "Image" tab
2. Upload a WhatsApp screenshot or meme
3. System extracts text using OCR
4. Visual forensics checks for manipulation
5. Claims are verified

### Video/YouTube Verification
1. Go to "Video" tab or "URL" tab
2. Upload video or paste YouTube URL
3. First 30 seconds are transcribed
4. Claims extracted and verified

## 🔧 Troubleshooting

### "Import error: whisper"
```powershell
pip install openai-whisper
```

### "FFmpeg not found"
- Ensure FFmpeg is in PATH
- Restart terminal after installation

### "Tesseract not found"
- Install Tesseract OCR
- Add to system PATH
- Restart terminal

### "Gemini API error"
- Check your API key in .env
- Verify key is valid at https://ai.google.dev/
- Check quota/limits

### "DuckDuckGo search failed"
- Check internet connection
- Try again (rate limiting)
- Alternative: implement Google Custom Search

## 📊 API Endpoints

### POST /api/verify/text
```json
{
  "text": "Your claim here",
  "views": 1000,
  "likes": 100
}
```

### POST /api/verify/url
```
url=https://example.com/article
```

### POST /api/verify/image
```
file=<image_file>
```

### GET /api/result/{job_id}
Get verification results

### GET /api/download/{job_id}/{claim_id}
Download PDF receipt

## 🌍 Supported Languages

**Full Support (with translation):**
- English
- Hindi (हिंदी)
- Marathi (मराठी)

**Partial Support (English output):**
- Gujarati, Tamil, Telugu, Bengali, Kannada, Malayalam, Punjabi, Urdu

## 📦 Project Structure

```
MumbaiHacks/
├── agents/              # 6 AI agents
│   ├── agent1_ingestion.py
│   ├── agent2_claims.py
│   ├── agent3_evidence.py
│   ├── agent4_verification.py
│   ├── agent5_virality.py
│   └── agent6_synthesis.py
├── utils/               # Shared utilities
│   ├── llm_provider.py
│   ├── translator.py
│   └── visual_forensics.py
├── data/                # Credibility database
├── temp/                # Temporary files
├── receipts/            # PDF receipts
├── app.py               # Streamlit UI
├── backend.py           # FastAPI server
└── pipeline.py          # Pipeline controller
```

## 🎯 Key Features

✅ Multi-format input (text, image, video, PDF, URL)
✅ Visual forensics (ELA analysis)
✅ Multilingual support (11+ Indian languages)
✅ Web evidence retrieval with credibility scoring
✅ LLM-powered verification (Gemini)
✅ Virality & risk analysis
✅ PDF verification receipts
✅ Agent workflow transparency

## 💡 Tips

- For best results, provide social metrics (views, likes, shares)
- High-quality images work better for OCR
- YouTube videos are processed quickly (30 seconds)
- Check agent workflow for transparency
- Download PDF receipts for official records

## 🆘 Support

For issues:
1. Check logs in `logs/` directory
2. Verify .env configuration
3. Ensure all system dependencies installed
4. Check API quota/limits

## 📝 License

MIT License - Built for Mumbai Hacks 2025
