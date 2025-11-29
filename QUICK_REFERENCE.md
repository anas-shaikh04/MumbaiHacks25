# 🛡️ VERITAS GUARDIAN - QUICK REFERENCE CARD

## ⚡ 30-Second Setup
```powershell
.\setup.ps1                    # Auto-install everything
# Edit .env → Add GEMINI_API_KEY
.\run.ps1 ui                   # Launch app
```

## 🎯 What It Does
Takes **any content** (text/image/video/PDF/URL) → Verifies using **6 AI agents** → Returns **True/False/Neutral** with confidence, evidence, risk level, and PDF receipt.

## 🤖 6 Agents
1. **Ingestion** - Extract text from any media
2. **Claims** - Detect language, extract facts
3. **Evidence** - Search trusted sources
4. **Verification** - AI fact-checking
5. **Virality** - Risk scoring
6. **Synthesis** - Generate reports

## 🚀 Run Commands
```powershell
# Start UI
streamlit run app.py

# Start API
uvicorn backend:app --reload

# Run tests
python scripts/test_system.py

# Check system
python scripts/check_system.py
```

## 📊 Input Types
- 📝 **Text** - Plain text, tweets, messages
- 🔗 **URL** - News articles, YouTube videos
- 🖼️ **Image** - Screenshots, memes (OCR)
- 🎥 **Video** - Video files (speech-to-text)
- 📄 **PDF** - Documents

## 🌍 Languages Supported
**Full:** English, Hindi (हिंदी), Marathi (मराठी)
**Partial:** Gujarati, Tamil, Telugu, Bengali, Kannada, Malayalam, Punjabi, Urdu

## 📦 Key Dependencies
- **Gemini API** - LLM verification
- **Whisper** - Speech-to-text
- **FFmpeg** - Video/audio processing
- **Tesseract** - Image OCR
- **Streamlit** - Web UI
- **FastAPI** - REST API

## 🔧 System Requirements
- Python 3.9+
- FFmpeg (https://ffmpeg.org/download.html)
- Tesseract (https://github.com/UB-Mannheim/tesseract/wiki)
- Gemini API key (https://ai.google.dev/)

## 📂 Important Files
- `app.py` - Streamlit UI
- `backend.py` - FastAPI server
- `pipeline.py` - Agent controller
- `.env` - Configuration (API keys)
- `data/credibility.csv` - Trusted sources

## 🔗 API Endpoints
```
POST   /api/verify/text          - Verify text
POST   /api/verify/url           - Verify URL
POST   /api/verify/image         - Verify image
POST   /api/verify/video         - Verify video
POST   /api/verify/pdf           - Verify PDF
GET    /api/result/{job_id}      - Get results
GET    /api/download/{job}/{clm} - Download PDF
```

## 🧪 Test Claims
```python
"5G towers cause COVID-19"                    # English
"5G के टावर कोरोना फैला रहे हैं"              # Hindi
"Vaccines contain microchips"                 # English
```

## 📈 Output Format
```json
{
  "user_label": "False",
  "confidence": 95,
  "short_explain_en": "Debunked by WHO",
  "virality_score": 82,
  "combined_risk_level": "critical",
  "evidence": [...],
  "receipt_pdf_path": "receipts/clm_001.pdf"
}
```

## ⚠️ Troubleshooting
| Problem | Solution |
|---------|----------|
| Import whisper failed | `pip install openai-whisper` |
| FFmpeg not found | Install & add to PATH |
| Gemini API error | Check API key in .env |
| DuckDuckGo failed | Check internet connection |

## 📚 Documentation
- `README.md` - Main docs
- `SETUP_GUIDE.md` - Setup help
- `API_DOCUMENTATION.md` - API reference
- `FINAL_SUMMARY.md` - Complete overview

## 💡 Demo Tips
1. Start with simple text claim
2. Show Hindi input → English output
3. Upload WhatsApp screenshot
4. Display agent workflow
5. Download PDF receipt
6. Highlight risk levels

## 🎯 Risk Levels
- 🟢 **Low** - True or low virality
- 🟡 **Medium** - Neutral or moderate spread
- 🟠 **High** - False with medium virality
- 🔴 **Critical** - False with high virality

## ✅ Pre-Demo Checklist
- [ ] Gemini API key configured
- [ ] FFmpeg & Tesseract installed
- [ ] Virtual environment active
- [ ] System tests pass
- [ ] Test claim works end-to-end
- [ ] PDF generation works

## 🏆 Key Features
✅ Multi-format (5 types)
✅ Multilingual (11+ languages)
✅ Visual forensics
✅ LLM verification
✅ Virality analysis
✅ PDF receipts
✅ REST API
✅ Web UI

## 📞 Quick Help
```powershell
# Full system check
python scripts/check_system.py

# Component tests
python scripts/test_system.py

# View logs
Get-Content logs/*.log
```

## 🎉 Ready to Go!
```powershell
# 1. Setup
.\setup.ps1

# 2. Configure
# Edit .env, add GEMINI_API_KEY

# 3. Run
.\run.ps1 ui

# 4. Test
# Go to http://localhost:8501
# Input: "5G towers cause COVID-19"
# Click: "Verify Text"
# See: Results with verdict, confidence, evidence, risk
```

---

**For Mumbai Hacks 2025**
Built with ❤️ in India
