# 🛡️ Veritas Guardian - Complete React Migration Guide

## 📋 Table of Contents
- [Overview](#overview)
- [What Changed](#what-changed)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Features](#features)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Your **Veritas Guardian** multi-agent misinformation verification system now has a modern React frontend that:
- ✅ Replaces the Streamlit UI
- ✅ Keeps all existing functionality
- ✅ Adds enhanced user experience
- ✅ Works with the existing backend
- ✅ Includes all 6 AI agents workflow

## 🆕 What Changed

### New Files
1. **`frontend/src/pages/VerificationPage.tsx`** - Main verification interface (830+ lines)
2. **`frontend/src/pages/VerificationPage.module.css`** - Complete styling (550+ lines)
3. **`frontend/FRONTEND_GUIDE.md`** - Detailed documentation
4. **`MIGRATION_SUMMARY.md`** - Migration overview
5. **`setup-frontend.ps1`** - Quick setup script

### Modified Files
1. **`frontend/src/App.tsx`** - Added `/verify` route
2. **`frontend/src/components/HeaderDifs/Header.tsx`** - Added navigation link
3. **`backend.py`** - Added job status endpoint

### Unchanged (Still Working)
- All 6 agent files in `agents/`
- Pipeline logic in `pipeline.py`
- Existing frontend pages (Body, Messages, File, Quiz)
- Backend verification logic
- Database and utils

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```powershell
# Run the setup script
.\setup-frontend.ps1
```

This will:
1. Check Node.js/npm installation
2. Install all dependencies
3. Optionally start the dev server

### Option 2: Manual Setup

```powershell
# 1. Install frontend dependencies
cd frontend
npm install

# 2. Start backend (in one terminal)
cd ..
python backend.py

# 3. Start frontend (in another terminal)
cd frontend
npm run dev
```

### Access the App
- **Main verification page**: http://localhost:5173/verify
- **Simple text detection**: http://localhost:5173/
- **Message check**: http://localhost:5173/messages
- **File upload**: http://localhost:5173/file
- **Quiz**: http://localhost:5173/quiz

## 📖 Detailed Setup

### Prerequisites
- **Node.js** 16+ (with npm)
- **Python** 3.8+
- All Python dependencies installed (from requirements.txt)

### Step-by-Step Installation

#### 1. Check Node.js
```powershell
node --version  # Should show v16+ or higher
npm --version   # Should show 7+ or higher
```

If not installed, download from: https://nodejs.org/

#### 2. Install Frontend Dependencies
```powershell
cd frontend
npm install
```

This installs:
- React 18
- React Router DOM
- Framer Motion (animations)
- Axios (API calls)
- TypeScript
- Vite (build tool)
- And all other dependencies

#### 3. Start Backend
```powershell
# From project root
python backend.py
```

Backend will start on `http://localhost:8000`

Verify it's running:
```powershell
curl http://localhost:8000
# Should return: {"status":"online","service":"Veritas Guardian API","version":"1.0.0"}
```

#### 4. Start Frontend
```powershell
cd frontend
npm run dev
```

Frontend will start on `http://localhost:5173` (or next available port)

## ✨ Features

### Input Methods (5 Types)

#### 1. Text Verification
- Paste any text, tweet, message, or claim
- Add metadata: views, likes, shares, comments
- Instant verification

#### 2. URL Verification
- Enter any article URL or YouTube link
- Automatic content extraction
- Full analysis

#### 3. Image Verification
- Upload screenshots, memes, images with text
- OCR text extraction
- Visual forensics analysis
- Live preview before verification

#### 4. Video Verification
- Upload video files (MP4, AVI, MOV, etc.)
- Audio transcription
- First 30 seconds analyzed
- Video preview

#### 5. PDF Verification
- Upload PDF documents
- Text extraction from all pages
- Full content analysis
- File size display

### Results Display

#### Summary Metrics
- **Total Claims**: Number of verifiable claims found
- **True Count**: ✅ Verified true claims
- **False Count**: ❌ Verified false claims
- **Neutral Count**: ⚠️ Unverifiable/neutral claims
- **Risk Level**: 🟢 Low / 🟡 Medium / 🟠 High / 🔴 Critical

#### Individual Claims
Each claim shows:
- **Claim text** (what was fact-checked)
- **Verdict** (True/False/Neutral)
- **Confidence** (percentage)
- **Explanation** (in local language + English)
- **Virality Score** (1-100)
- **Risk Level** (with color coding)
- **Evidence Sources** (collapsible list)
- **PDF Receipt** (downloadable)
- **Human Review Flag** (if needed)

#### Additional Info
- Language detection and support level
- Visual forensics warnings (if manipulation detected)
- Source credibility scores
- Full evidence URLs

## 📱 Usage Guide

### Basic Workflow

1. **Navigate to Verification Page**
   - Click hamburger menu (☰)
   - Select "🛡️ Veritas Guardian (Full Verification)"
   - Or go directly to: http://localhost:5173/verify

2. **Select Input Type**
   - Click one of the tabs: 📝 Text / 🔗 URL / 🖼️ Image / 🎥 Video / 📄 PDF

3. **Enter Your Content**
   - Text: Paste content and optionally add metadata
   - URL: Enter the web address
   - File: Click to upload or drag & drop

4. **Click Verify**
   - Button shows "🔍 Verify [Type]"
   - Loading spinner appears
   - Wait for processing (10-60 seconds typically)

5. **View Results**
   - Summary appears at top
   - Scroll down for individual claims
   - Click evidence to expand
   - Download PDF receipts as needed

### Settings Panel (Sidebar)

#### About Section
- Shows information about 6 AI agents
- Explains the verification process

#### Settings
- **Show Agent Workflow**: Toggle to see behind-the-scenes agent actions
- **Show All Evidence**: Toggle to expand/collapse evidence by default

### Tips for Best Results

#### Text Input
- Longer text = more context = better analysis
- Include full sentences, not just keywords
- Add metadata if available (views, shares) for virality analysis

#### URL Input
- Use full URLs with http:// or https://
- Works with articles, YouTube, social media
- May take longer for video transcription

#### Image Upload
- Clear, readable text works best
- Supported: PNG, JPG, JPEG
- OCR works on screenshots, memes, infographics

#### Video Upload
- First 30 seconds are analyzed
- Supported: MP4, AVI, MOV, MKV
- Audio is transcribed automatically

#### PDF Upload
- Works with all pages
- Text-based PDFs work best
- Scanned PDFs use OCR

## 🔌 API Documentation

### Endpoints Used by Frontend

#### 1. Verify Text
```http
POST /api/verify/text
Content-Type: application/json

{
  "text": "Your text here",
  "views": 1000,      // optional
  "likes": 100,       // optional
  "shares": 50,       // optional
  "comments": 20      // optional
}

Response: { "job_id": "uuid", "status": "pending" }
```

#### 2. Verify URL
```http
POST /api/verify/url
Content-Type: multipart/form-data

url=https://example.com/article

Response: { "job_id": "uuid", "status": "pending" }
```

#### 3. Verify Image
```http
POST /api/verify/image
Content-Type: multipart/form-data

file=<binary data>

Response: { "job_id": "uuid", "status": "pending" }
```

#### 4. Verify Video
```http
POST /api/verify/video
Content-Type: multipart/form-data

file=<binary data>

Response: { "job_id": "uuid", "status": "pending" }
```

#### 5. Verify PDF
```http
POST /api/verify/pdf
Content-Type: multipart/form-data

file=<binary data>

Response: { "job_id": "uuid", "status": "pending" }
```

#### 6. Check Job Status
```http
GET /api/job/{job_id}/status

Response: {
  "job_id": "uuid",
  "status": "pending|processing|completed|failed",
  "progress": "Agent X is working...",
  "result": { ... },  // only when completed
  "error": "..."      // only when failed
}
```

### Job Polling Logic

```typescript
// Frontend polls every 2 seconds
// Maximum 60 attempts (2 minutes)
// Stops when status is "completed" or "failed"

const poll = async () => {
  const response = await fetch(`/api/job/${jobId}/status`);
  const data = await response.json();
  
  if (data.status === "completed") {
    // Display results
    setResult(data.result);
  } else if (data.status === "failed") {
    // Show error
    alert(data.error);
  } else {
    // Continue polling after 2 seconds
    setTimeout(poll, 2000);
  }
};
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Cannot find module 'react'" errors
**Problem**: Dependencies not installed
**Solution**:
```powershell
cd frontend
npm install
```

#### 2. "CORS error" in browser console
**Problem**: Backend CORS not configured for frontend URL
**Solution**: Update `backend.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. "Connection refused" to http://localhost:8000
**Problem**: Backend not running
**Solution**:
```powershell
# Start backend first
python backend.py
```

#### 4. Frontend stuck on "Loading..."
**Problem**: Job polling not working or backend slow
**Solution**:
- Check backend console for errors
- Verify backend is processing the job
- Check network tab in browser DevTools
- Increase timeout in `VerificationPage.tsx` (line ~175)

#### 5. File upload fails
**Problem**: File size too large or unsupported format
**Solution**:
- Check file size (backend may have limits)
- Verify file format matches accepted types
- Check backend console for error messages

#### 6. Results not displaying
**Problem**: Response format mismatch
**Solution**:
- Check browser console for errors
- Verify backend response matches expected format
- Check `result` object structure in Network tab

### Debug Mode

#### Enable Console Logging
Add to `VerificationPage.tsx`:
```typescript
console.log("Job ID:", jobId);
console.log("Status:", data.status);
console.log("Result:", data.result);
```

#### Check Backend Logs
```powershell
# Backend logs are in:
logs/
└── app_YYYYMMDD.log
```

#### Browser DevTools
1. Open DevTools (F12)
2. Go to Network tab
3. Filter by "Fetch/XHR"
4. Check request/response for each API call

## 📊 Performance Tips

### Frontend
- Use production build for deployment: `npm run build`
- Images/videos are previewed locally (not uploaded to backend until verify)
- Results are cached in component state

### Backend
- Jobs are processed asynchronously
- Multiple requests can be handled concurrently
- Cleanup old jobs periodically (add cron job)

## 🎨 Customization

### Changing Colors
Edit `VerificationPage.module.css`:
```css
/* Verdict colors */
.verdict-true { background-color: #d4edda; }  /* Green */
.verdict-false { background-color: #f8d7da; } /* Red */
.verdict-neutral { background-color: #fff3cd; } /* Yellow */

/* Risk colors */
.risk-low { color: #28a745; }      /* Green */
.risk-medium { color: #ffc107; }   /* Yellow */
.risk-high { color: #fd7e14; }     /* Orange */
.risk-critical { color: #dc3545; } /* Red */
```

### Adding New Input Type
1. Add tab in `VerificationPage.tsx`:
```typescript
<button className={styles.tab} onClick={() => setActiveTab("newtype")}>
  🆕 New Type
</button>
```

2. Add content section:
```typescript
{activeTab === "newtype" && (
  <div>
    {/* Your input UI */}
  </div>
)}
```

3. Add backend endpoint in `backend.py`:
```python
@app.post("/api/verify/newtype")
async def verify_newtype(...):
    # Processing logic
    pass
```

### Changing Polling Interval
Edit `VerificationPage.tsx` line ~180:
```typescript
await new Promise((resolve) => setTimeout(resolve, 2000)); // Change 2000 to desired ms
```

### Changing Timeout
Edit `VerificationPage.tsx` line ~165:
```typescript
const maxAttempts = 60; // Change to desired number
```

## 🚀 Deployment

### Frontend (Static Hosting)

```powershell
# Build for production
cd frontend
npm run build

# Output is in: frontend/dist/
# Deploy this folder to:
# - Vercel
# - Netlify
# - GitHub Pages
# - Any static hosting
```

### Backend (Server Hosting)

```powershell
# Use Gunicorn or Uvicorn
uvicorn backend:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables

Create `.env` file in frontend:
```env
VITE_API_URL=http://your-backend-url.com
```

Update API calls to use:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

## 📚 Additional Resources

- **Vite Documentation**: https://vitejs.dev/
- **React Router**: https://reactrouter.com/
- **Framer Motion**: https://www.framer.com/motion/
- **TypeScript**: https://www.typescriptlang.org/

## 🎉 Success!

You now have a fully functional React frontend for Veritas Guardian! 

**Key Points:**
- ✅ All Streamlit features migrated
- ✅ Enhanced UI/UX with animations
- ✅ Fully responsive design
- ✅ Type-safe TypeScript code
- ✅ Production-ready build system
- ✅ Comprehensive documentation

**Next Steps:**
1. Test all verification types
2. Customize colors/styling if desired
3. Add more features as needed
4. Deploy to production

Enjoy your modern React-powered Veritas Guardian! 🛡️
