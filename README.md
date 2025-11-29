# 🛡️ VERITAS GUARDIAN

**Multi-Agent, Multimodal, Multilingual Misinformation Verification System**

Built for Mumbai Hacks 2025 | India-First AI Solution

---

## 📌 One-Line Description

Veritas Guardian is a **6-agent AI system** that verifies any content (text, images, videos, URLs, PDFs), extracts factual claims, searches trusted evidence, and delivers **True/False/Neutral verdicts** with confidence scores, risk levels, multilingual explanations, and PDF verification receipts.

---

## ✨ Key Features

- 🎯 **Multi-Format Input**: Text, URLs, Images, Videos, PDFs
- 🌍 **Multilingual**: 11+ Indian languages (Hindi, Marathi, Gujarati, Tamil, Bengali, etc.)
- 🔍 **Visual Forensics**: ELA analysis for image manipulation detection
- 🌐 **Web Evidence**: Auto-searches trusted sources (WHO, PIB, fact-checkers)
- 🤖 **Gemini AI**: LLM-powered verification with reasoning
- 📊 **Virality Analysis**: Risk scoring (low/medium/high/critical)
- 📄 **PDF Receipts**: Downloadable verification certificates
- 🔬 **Transparency**: Full agent workflow visibility

---

## 🚀 Quick Start (Windows)

### Automated Setup
```powershell
# Run setup script (installs everything)
.\setup.ps1
```

### Manual Setup
```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
Copy-Item .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Initialize database
python scripts/init_credibility_db.py
```

### System Requirements
- **Python 3.9+**
- **FFmpeg** (for video/audio): https://ffmpeg.org/download.html
- **Tesseract OCR** (for images): https://github.com/UB-Mannheim/tesseract/wiki

### Run Application
```powershell
# Streamlit UI (recommended for demo)
streamlit run app.py

# OR FastAPI backend
uvicorn backend:app --reload --port 8000
```

---

## 🏗️ System Architecture

### 6-Agent Pipeline

```
User Input → [Agent 1] → [Agent 2] → [Agent 3] → [Agent 4] → [Agent 5] → [Agent 6] → Results
             Ingestion   Claims      Evidence    Verify      Virality    Synthesis
```

#### **Agent 1: Ingestion & Multimodal Processing**
- Extracts text from any media type
- OCR for images (EasyOCR + Tesseract)
- Speech-to-text for videos (Whisper)
- Visual forensics (ELA analysis)
- **Tech**: PyMuPDF, pdfplumber, yt-dlp, OpenAI Whisper

#### **Agent 2: Language Detection & Claim Extraction**
- Detects language (langdetect)
- Translates to English (Gemini)
- Extracts factual claims using LLM
- **Tech**: langdetect, Gemini API

#### **Agent 3: Evidence Retrieval**
- Searches DuckDuckGo for evidence
- Filters by credibility database
- Prioritizes govt/health/fact-check sources
- **Tech**: duckduckgo-search, pandas

#### **Agent 4: Verification & Labeling**
- LLM reasoning with evidence
- Confidence scoring (0-100)
- Maps to True/False/Neutral
- Safety rules for sensitive topics
- **Tech**: Gemini API, custom logic

#### **Agent 5: Virality & Risk Analysis**
- Computes virality score (reach + engagement + content)
- Determines risk level (low/medium/high/critical)
- **Tech**: NumPy, custom algorithms

#### **Agent 6: Response Synthesis & PDF**
- Translates explanations to original language
- Generates PDF verification receipts
- Builds final UI-ready results
- **Tech**: ReportLab, Gemini API

---

## 📁 Project Structure

```
MumbaiHacks/
├── agents/                      # 6 AI agents
│   ├── agent1_ingestion.py     # Media processing
│   ├── agent2_claims.py        # Language & claims
│   ├── agent3_evidence.py      # Web search
│   ├── agent4_verification.py  # LLM verification
│   ├── agent5_virality.py      # Risk analysis
│   └── agent6_synthesis.py     # PDF generation
├── utils/                       # Shared utilities
│   ├── llm_provider.py         # Gemini wrapper
│   ├── translator.py           # Multilingual support
│   └── visual_forensics.py     # ELA analysis
├── data/                        # Credibility database
│   └── credibility.csv         # Trusted sources
├── scripts/                     # Setup scripts
│   ├── setup.py                # Python setup
│   ├── init_credibility_db.py  # DB initialization
│   └── test_system.py          # Component tests
├── temp/                        # Temporary files
├── receipts/                    # PDF receipts
├── logs/                        # Application logs
├── app.py                       # Streamlit UI
├── backend.py                   # FastAPI server
├── pipeline.py                  # Pipeline controller
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── setup.ps1                    # Windows setup script
├── README.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup
└── API_DOCUMENTATION.md        # API reference
```

---

## 🌍 Supported Languages

| Language | Code | Support Level | Translation |
|----------|------|---------------|-------------|
| English  | en   | ✅ Full       | Native      |
| Hindi    | hi   | ✅ Full       | Yes         |
| Marathi  | mr   | ✅ Full       | Yes         |
| Gujarati | gu   | ⚠️ Partial    | Beta        |
| Tamil    | ta   | ⚠️ Partial    | Beta        |
| Telugu   | te   | ⚠️ Partial    | Beta        |
| Bengali  | bn   | ⚠️ Partial    | Beta        |
| Kannada  | kn   | ⚠️ Partial    | Beta        |
| Malayalam| ml   | ⚠️ Partial    | Beta        |
| Punjabi  | pa   | ⚠️ Partial    | Beta        |
| Urdu     | ur   | ⚠️ Partial    | Beta        |

---

## 📊 Usage Examples

### Example 1: Text Verification
```python
from pipeline import VeritasGuardianPipeline

pipeline = VeritasGuardianPipeline()

result = pipeline.process(
    "5G towers cause COVID-19",
    input_type="text",
    metadata={"views": 50000, "likes": 2000}
)

print(result['results'][0]['user_label'])  # "False"
print(result['results'][0]['confidence'])  # 95
```

### Example 2: Image Verification
```python
result = pipeline.process(
    "screenshot.jpg",
    input_type="image"
)
```

### Example 3: YouTube Video
```python
result = pipeline.process(
    "https://youtube.com/watch?v=...",
    input_type="url"
)
```

---

## 🔌 API Endpoints

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete reference.

**Key Endpoints:**
- `POST /api/verify/text` - Verify text content
- `POST /api/verify/url` - Verify URL/YouTube
- `POST /api/verify/image` - Verify image
- `POST /api/verify/video` - Verify video
- `POST /api/verify/pdf` - Verify PDF
- `GET /api/result/{job_id}` - Get results
- `GET /api/download/{job_id}/{claim_id}` - Download PDF

---

## 🧪 Testing

Run system tests:
```powershell
python scripts/test_system.py
```

Test individual agents:
```python
# Test Agent 1
from agents.agent1_ingestion import IngestionAgent
agent = IngestionAgent()
result = agent.ingest("Test text", "text")
```

---

## 🔑 API Keys

1. Get Gemini API key: https://ai.google.dev/
2. Add to `.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

---

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[.env.example](.env.example)** - Environment configuration

---

## 🛠️ Tech Stack

**Core AI:**
- Google Gemini (LLM)
- OpenAI Whisper (Speech-to-text)
- EasyOCR / Tesseract (OCR)

**Backend:**
- FastAPI (REST API)
- Python 3.9+
- Asyncio

**Frontend:**
- Streamlit (UI)

**Media Processing:**
- FFmpeg (video/audio)
- PyMuPDF / pdfplumber (PDF)
- Pillow (images)
- yt-dlp (YouTube)

**Data:**
- Pandas (credibility DB)
- DuckDuckGo Search (evidence)
- ReportLab (PDF generation)

---

## 🚨 Troubleshooting

### "Import whisper failed"
```powershell
pip install openai-whisper
```

### "FFmpeg not found"
- Install FFmpeg: https://ffmpeg.org/download.html
- Add to system PATH
- Restart terminal

### "Gemini API error"
- Check API key in `.env`
- Verify key at https://ai.google.dev/
- Check usage quota

### "No module named 'agents'"
```powershell
# Ensure you're in project root
cd MumbaiHacks
python pipeline.py
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

---

## 🎯 Roadmap

- [ ] Add more Indian language models
- [ ] Implement user authentication
- [ ] Add claim history/database
- [ ] Real-time social media monitoring
- [ ] Mobile app (React Native)
- [ ] Chrome extension
- [ ] WhatsApp bot integration

---

## 👥 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Submit pull request

---

## 📄 License

MIT License - See LICENSE file

---

## 🏆 Built For

**Mumbai Hacks 2025**
India's Premier Hackathon

**Team:** Veritas Guardian
**Mission:** Combat misinformation with AI

---

## 📞 Support

- GitHub Issues: [Report bugs](https://github.com/...)
- Documentation: See `docs/` folder
- Email: support@veritasguardian.ai

---

## ⭐ Acknowledgments

- Google Gemini API
- OpenAI Whisper
- DuckDuckGo Search
- Indian fact-checking organizations (AltNews, BoomLive, Vishvas News)

---

**Built with ❤️ in India**
