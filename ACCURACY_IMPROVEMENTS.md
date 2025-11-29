# Accuracy Improvements & Detection Guide

## Overview
This document explains how content detection works, recent accuracy improvements, and troubleshooting tips for the Veritas Guardian system.

## 🎯 Recent Improvements

### 1. **Enhanced Image Detection (OCR)**

**What Changed:**
- Added detailed logging to track OCR performance
- Improved error handling with specific messages
- Added text length validation (minimum 10 characters)
- Better fallback mechanism between EasyOCR and Tesseract

**How It Works:**
1. **EasyOCR (Primary)**: Supports English + Hindi, better for multilingual text
2. **Tesseract (Fallback)**: Supports English + Hindi + Marathi, used if EasyOCR fails
3. **Visual Forensics**: Analyzes image for manipulation (runs in parallel)

**Error Messages You Might See:**
- `"No readable text found in image"` → Image contains only graphics or is too blurry
- `"Error processing image. Please ensure the image is clear and contains readable text"` → File corrupted or unsupported format

**Tips for Better Results:**
- Use high-resolution images (minimum 800x600)
- Ensure text is clearly visible and not at extreme angles
- Avoid heavily compressed or filtered images
- Supported formats: JPG, PNG, WEBP

---

### 2. **Improved URL/News Detection**

**What Changed:**
- Smarter content extraction (looks for `<article>`, `<main>`, `.article-body`)
- Removes navigation, footer, and header clutter
- Better handling of paywalls and JavaScript-heavy sites
- Extracts headlines and combines with body text
- Increased minimum content threshold to 50 characters

**How It Works:**
1. Sends request with browser-like headers to avoid blocking
2. Parses HTML and removes non-content elements (nav, footer, scripts)
3. Finds article content in order of priority:
   - `<article>` tags
   - `<main>` tags
   - `.article-body` class
   - All `<p>` tags as fallback
4. Extracts headline from `<h1>` and prepends to content
5. Limits to 5000 characters for processing efficiency

**Error Messages You Might See:**
- `"Unable to extract meaningful content from URL"` → Paywall, JavaScript-required, or no text content
- `"Request timed out"` → Website took longer than 15 seconds to respond
- `"Unable to access URL"` → Connection error, blocked by website, or invalid URL

**Tips for Better Results:**
- Use direct article URLs, not homepage URLs
- Avoid paywalled content (WSJ, NYT premium, etc.)
- Some sites block automated access - try different sources
- YouTube URLs are handled separately (see Video Detection below)

---

### 3. **Enhanced Video Detection**

**What Changed:**
- Added audio quality validation (checks file size)
- Better Whisper transcription with language auto-detection
- Improved logging to track processing steps
- Returns detected language in results
- Better cleanup of temporary files

**How Video Detection Works:**

```
Video File → FFmpeg Extraction → Whisper Transcription → Text Output
```

**Step-by-Step Process:**
1. **Audio Extraction** (FFmpeg):
   - Extracts first 30 seconds of audio
   - Converts to MP3 format at 16kHz sample rate
   - Optimized for speech recognition

2. **Transcription** (Whisper "tiny" model):
   - Auto-detects language (supports 90+ languages)
   - Transcribes speech to text
   - Fast processing (~5-10 seconds for 30 seconds of video)

3. **Quality Checks**:
   - Validates audio file size (must be > 1KB)
   - Checks transcription length (minimum 10 characters)
   - Returns meaningful error if no speech detected

**Error Messages You Might See:**
- `"Video contains no detectable audio or speech"` → Silent video or no clear speech in first 30 seconds
- `"Unable to extract audio from video"` → Unsupported video format or corrupted file
- `"Error processing video. Ensure ffmpeg is installed"` → FFmpeg not found in system PATH

**Tips for Better Accuracy:**
- Ensure video has clear audio in the first 30 seconds
- Background noise and music can reduce accuracy
- Supported formats: MP4, AVI, MOV, MKV, WebM
- For best results, use videos with:
  - Clear speech (not mumbling or whispering)
  - Minimal background noise
  - Standard accents and dialects

**Improving Transcription Accuracy:**
If you need better accuracy, upgrade the Whisper model in `agents/agent1_ingestion.py`:

```python
# Current (fast, 75MB):
self.whisper_model = whisper.load_model("tiny")

# Better accuracy (slower, 461MB):
self.whisper_model = whisper.load_model("base")

# Best accuracy (slowest, 1.5GB):
self.whisper_model = whisper.load_model("small")
```

---

### 4. **Multilingual Language Support**

**What Changed:**
- Better language detection with confidence checking
- Validates text length before detection (minimum 10 characters)
- Improved error handling for ambiguous languages
- Skips claim extraction for error messages

**Supported Languages:**
- **English** (en) - Primary
- **Hindi** (hi) - Fully supported
- **Marathi** (mr) - Fully supported
- **Other languages** - Auto-detected and translated to English for processing

**How It Works:**
1. **Language Detection** (langdetect library):
   - Analyzes text and returns ISO 639-1 language code
   - Requires minimum 10 characters for reliable detection
   - Defaults to English if uncertain

2. **Translation** (Google Translate via utils/translator.py):
   - Translates non-English text to English
   - Preserves original text for reference
   - Used for internal claim extraction

3. **Claim Extraction**:
   - LLM processes English text
   - Extracts factual claims (maximum 3)
   - Returns both original and canonical (English) versions

**Error Handling:**
- Text too short → Defaults to English
- Ambiguous language → Defaults to English with warning
- Error messages from ingestion → Skips claim extraction

---

## 🔍 How to Test Improvements

### Test Image Detection:
```python
# Upload clear image with text in English, Hindi, or Marathi
# Check logs for:
# - "EasyOCR extracted: X characters"
# - "Tesseract extracted: X characters" (if fallback)
```

### Test URL Detection:
```python
# Try different news sources:
# - https://www.bbc.com/news/...
# - https://www.theguardian.com/...
# - https://indianexpress.com/...
# 
# Check logs for:
# - "Extracted X characters from URL"
```

### Test Video Detection:
```python
# Upload video with clear speech
# Check logs for:
# - "Extracting audio from video..."
# - "Transcribing video audio..."
# - "Transcribed X characters, language: Y"
```

### Test Multilingual:
```python
# Try text in Hindi/Marathi
# Check logs for:
# - "Detected primary language: Hindi/Marathi"
# - Translation confirmation
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Failed to verify" with images
**Possible Causes:**
- Image is too blurry or low resolution
- Text is at extreme angle or curved
- Image format not supported

**Solutions:**
- Use higher resolution images
- Ensure text is horizontal and clearly visible
- Try JPG or PNG format

---

### Issue 2: "Unable to extract content" from URLs
**Possible Causes:**
- Website behind paywall
- JavaScript-heavy website
- Website blocking automated requests
- Not a news article URL

**Solutions:**
- Try different news sources
- Use direct article URLs
- Check if URL is accessible in browser
- For YouTube, system handles it automatically

---

### Issue 3: "No speech detected" in videos
**Possible Causes:**
- Video has no audio track
- Speech doesn't start in first 30 seconds
- Audio quality too poor
- Heavy background noise

**Solutions:**
- Ensure video has audio
- Trim video so speech starts early
- Use clearer audio recording
- Consider upgrading Whisper model (see above)

---

### Issue 4: Wrong language detected
**Possible Causes:**
- Mixed language content
- Text too short for detection
- Ambiguous words similar across languages

**Solutions:**
- Use longer text samples
- Ensure text is primarily in one language
- System defaults to English when uncertain

---

## 📊 Performance Expectations

### Processing Times (approximate):
- **Text**: Instant (<1 second)
- **URLs**: 2-5 seconds (network dependent)
- **Images**: 3-8 seconds (OCR + forensics)
- **Videos**: 10-20 seconds (audio extraction + transcription)
- **PDFs**: 2-5 seconds per page

### Accuracy Rates:
- **OCR (clear text)**: 90-95%
- **OCR (poor quality)**: 60-80%
- **URL extraction**: 85-90% (varies by website)
- **Video transcription (tiny model)**: 70-85%
- **Language detection**: 90-95%

---

## 🚀 Future Improvements

### Short-term:
1. Add newspaper3k library for better article extraction
2. Implement frame-by-frame OCR for text in videos
3. Add more OCR languages (Gujarati, Tamil, etc.)
4. Improve error messages with actionable suggestions

### Medium-term:
1. Upgrade Whisper model to "base" or "small"
2. Add audio preprocessing (noise reduction)
3. Implement content caching to avoid re-processing
4. Add support for more video formats

### Long-term:
1. Fine-tune LLM for Indian news content
2. Add real-time video analysis
3. Implement multi-modal verification (text + image + audio)
4. Add support for live streams

---

## 📝 Logging & Debugging

All improvements include detailed logging. Check `logs/` directory for:

- `agent1_ingestion.log` - Content extraction details
- `agent2_claims.log` - Claim extraction process
- `backend.log` - API request handling

**Key Log Messages:**
```
[INFO] Processing image: /path/to/image.jpg
[INFO] Attempting OCR with EasyOCR...
[INFO] EasyOCR extracted: 245 characters
[INFO] Language detected: hi
[INFO] Requesting claim extraction from LLM...
[INFO] Extracted 3 claims
```

---

## 🆘 Support

If you continue experiencing issues after these improvements:

1. Check the logs in `logs/` directory
2. Verify FFmpeg is installed: `ffmpeg -version`
3. Verify Tesseract is installed: `tesseract --version`
4. Ensure all Python dependencies are up to date: `pip install -r requirements.txt --upgrade`
5. Check that backend is running: `curl http://localhost:8000/health`

For debugging, enable verbose logging by setting `LOGURU_LEVEL=DEBUG` in your environment.
