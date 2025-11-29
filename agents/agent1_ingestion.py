"""
Agent 1: Ingestion & Multimodal Processing
Extracts text from any input type: text, URL, image, video, PDF
Performs visual forensics on images/videos
"""

import os
import subprocess
from typing import Dict, Any, List
from pathlib import Path
from loguru import logger

# Media processing
import whisper
import pytesseract
import easyocr
from PIL import Image
import fitz  # PyMuPDF
import pdfplumber
from bs4 import BeautifulSoup
import requests
import yt_dlp
import cv2

# Utilities'
from utils.visual_forensics import analyze_image_forensics


class IngestionAgent:
    """
    Agent 1: Ingests and processes multimodal content
    Converts any input to structured text chunks
    """
    
    def __init__(self, temp_dir: str = "./temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        
        # Load Whisper model (tiny for speed)
        logger.info("Loading Whisper model...")
        self.whisper_model = whisper.load_model("tiny")
        
        # Initialize EasyOCR
        logger.info("Initializing EasyOCR reader...")
        self.ocr_reader = easyocr.Reader(['en', 'hi'], gpu=False)
        logger.success("IngestionAgent initialized successfully")
        logger.info("Whisper model loaded")
        
    def ingest(self, content: Any, input_type: str) -> Dict[str, Any]:
        """
        Main ingestion method - routes to appropriate processor
        
        Args:
            content: Input content (text string, file path, or URL)
            input_type: One of: "text", "url", "image", "video", "pdf"
            
        Returns:
            {
                "media_type": str,
                "chunks": [{"text": str, "timestamp": float, "media_type": str}],
                "visual_forensics": {"suspicion_level": str}
            }
        """
        logger.info(f"Starting ingestion for type: {input_type}")
        
        if input_type == "text":
            return self._process_text(content)
        elif input_type == "url":
            return self._process_url(content)
        elif input_type == "image":
            return self._process_image(content)
        elif input_type == "video":
            return self._process_video(content)
        elif input_type == "pdf":
            return self._process_pdf(content)
        else:
            raise ValueError(f"Unsupported input type: {input_type}")
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """Process plain text input"""
        logger.info("Processing text input")
        return {
            "media_type": "text",
            "chunks": [{
                "text": text,
                "timestamp": None,
                "media_type": "text"
            }],
            "visual_forensics": {"suspicion_level": "none"}
        }
    
    def _process_url(self, url: str) -> Dict[str, Any]:
        """Process URL - detects if YouTube or news article"""
        logger.info(f"Processing URL: {url}")
        
        if "youtube.com" in url or "youtu.be" in url:
            return self._process_youtube(url)
        else:
            return self._process_news_url(url)
    
    def _process_youtube(self, url: str) -> Dict[str, Any]:
        """Extract and transcribe YouTube video audio (first 30 seconds)"""
        logger.info(f"Processing YouTube video: {url}")
        
        output_path = self.temp_dir / "temp_audio.mp3"
        
        try:
            # Download audio using yt-dlp (first 30 seconds)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_path),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Transcribe with Whisper
            logger.info("Transcribing audio...")
            result = self.whisper_model.transcribe(str(output_path))
            
            # Clean up
            if output_path.exists():
                output_path.unlink()
            
            return {
                "media_type": "video",
                "chunks": [{
                    "text": result["text"],
                    "timestamp": 0,
                    "media_type": "video"
                }],
                "visual_forensics": {"suspicion_level": "low"}
            }
            
        except Exception as e:
            logger.error(f"YouTube processing failed: {e}")
            return {
                "media_type": "video",
                "chunks": [{
                    "text": f"Failed to process video: {str(e)}",
                    "timestamp": 0,
                    "media_type": "video"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
    
    def _process_news_url(self, url: str) -> Dict[str, Any]:
        """Extract text from news article URL"""
        logger.info(f"Processing news URL: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script, style, and nav elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            # Try to find article content
            article = soup.find('article') or soup.find('main') or soup.find(class_='article-body') or soup
            
            # Extract paragraphs from article
            paragraphs = article.find_all('p')
            text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip() and len(p.get_text().strip()) > 20])
            
            # Fallback: get all text if no paragraphs
            if not text or len(text) < 100:
                text = article.get_text()
                text = ' '.join(text.split())  # Clean whitespace
            
            # Extract headline if available
            headline = soup.find('h1')
            if headline:
                headline_text = headline.get_text().strip()
                text = f"{headline_text}. {text}"
            
            # Limit text length
            if len(text) > 5000:
                text = text[:5000] + "..."
            
            if not text or len(text) < 50:
                return {
                    "media_type": "url",
                    "chunks": [{
                        "text": "Unable to extract meaningful content from URL. The page may be behind a paywall or require JavaScript.",
                        "timestamp": None,
                        "media_type": "url"
                    }],
                    "visual_forensics": {"suspicion_level": "none"}
                }
            
            logger.info(f"Extracted {len(text)} characters from URL")
            
            return {
                "media_type": "url",
                "chunks": [{
                    "text": text,
                    "timestamp": None,
                    "media_type": "url"
                }],
                "visual_forensics": {"suspicion_level": "none"}
            }
            
        except requests.Timeout:
            logger.error("URL request timed out")
            return {
                "media_type": "url",
                "chunks": [{
                    "text": "Request timed out. The website took too long to respond.",
                    "timestamp": None,
                    "media_type": "url"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
        except requests.RequestException as e:
            logger.error(f"URL request failed: {e}")
            return {
                "media_type": "url",
                "chunks": [{
                    "text": f"Unable to access URL. Error: {str(e)}",
                    "timestamp": None,
                    "media_type": "url"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
        except Exception as e:
            logger.error(f"URL processing failed: {e}")
            return {
                "media_type": "url",
                "chunks": [{
                    "text": f"Error processing URL content.",
                    "timestamp": None,
                    "media_type": "url"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
    
    def _process_image(self, image_path: str) -> Dict[str, Any]:
        """Extract text from image using OCR and perform visual forensics"""
        logger.info(f"Processing image: {image_path}")
        
        try:
            # OCR text extraction
            img = Image.open(image_path)
            
            # Try EasyOCR for better multilingual support
            text = ""
            try:
                logger.info("Attempting OCR with EasyOCR...")
                result = self.ocr_reader.readtext(image_path)
                text = ' '.join([item[1] for item in result if item[1].strip()])
                logger.info(f"EasyOCR extracted: {len(text)} characters")
            except Exception as ocr_error:
                logger.warning(f"EasyOCR failed: {ocr_error}, trying Tesseract...")
                # Fallback to Tesseract
                try:
                    text = pytesseract.image_to_string(
                        img, 
                        lang='eng+hin+mar'
                    )
                    logger.info(f"Tesseract extracted: {len(text)} characters")
                except Exception as tess_error:
                    logger.error(f"Tesseract also failed: {tess_error}")
            
            # If no text extracted, return meaningful message
            if not text or len(text.strip()) < 10:
                text = "No readable text found in image. Image may contain only graphics or be too unclear for text extraction."
                logger.warning("Insufficient text extracted from image")
            
            # Visual forensics
            try:
                forensics = analyze_image_forensics(image_path)
            except Exception as forensics_error:
                logger.warning(f"Visual forensics failed: {forensics_error}")
                forensics = {"suspicion_level": "unknown"}
            
            return {
                "media_type": "image",
                "chunks": [{
                    "text": text.strip(),
                    "timestamp": None,
                    "media_type": "image"
                }],
                "visual_forensics": forensics
            }
            
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            return {
                "media_type": "image",
                "chunks": [{
                    "text": f"Error processing image. Please ensure the image is clear and contains readable text.",
                    "timestamp": None,
                    "media_type": "image"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
    
    def _process_video(self, video_path: str) -> Dict[str, Any]:
        """Extract audio from video and transcribe (first 30 seconds)"""
        logger.info(f"Processing video: {video_path}")
        
        audio_path = self.temp_dir / "temp_video_audio.mp3"
        
        try:
            logger.info("Extracting audio from video...")
            # Extract audio using ffmpeg (first 30 seconds)
            result = subprocess.run([
                'ffmpeg', '-i', video_path, '-t', '30',
                '-vn', '-acodec', 'libmp3lame',
                '-ar', '16000',  # Sample rate
                str(audio_path), '-y'
            ], check=True, capture_output=True, text=True)
            
            if not audio_path.exists() or audio_path.stat().st_size < 1000:
                logger.warning("Audio extraction produced no or minimal output")
                return {
                    "media_type": "video",
                    "chunks": [{
                        "text": "Video contains no detectable audio or speech in the first 30 seconds.",
                        "timestamp": 0,
                        "media_type": "video"
                    }],
                    "visual_forensics": {"suspicion_level": "medium"}
                }
            
            # Transcribe
            logger.info("Transcribing video audio...")
            transcript_result = self.whisper_model.transcribe(
                str(audio_path),
                language=None,  # Auto-detect
                task='transcribe'
            )
            
            transcribed_text = transcript_result["text"].strip()
            detected_lang = transcript_result.get("language", "unknown")
            
            logger.info(f"Transcribed {len(transcribed_text)} characters, language: {detected_lang}")
            
            # Clean up
            if audio_path.exists():
                audio_path.unlink()
            
            if not transcribed_text or len(transcribed_text) < 10:
                transcribed_text = "No clear speech detected in video audio."
            
            return {
                "media_type": "video",
                "chunks": [{
                    "text": transcribed_text,
                    "timestamp": 0,
                    "media_type": "video",
                    "detected_language": detected_lang
                }],
                "visual_forensics": {"suspicion_level": "medium"}
            }
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e.stderr}")
            return {
                "media_type": "video",
                "chunks": [{
                    "text": "Unable to extract audio from video. The video format may be unsupported.",
                    "timestamp": 0,
                    "media_type": "video"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
        except Exception as e:
            logger.error(f"Video processing failed: {e}")
            return {
                "media_type": "video",
                "chunks": [{
                    "text": f"Error processing video. Ensure ffmpeg is installed and the video format is supported.",
                    "timestamp": None,
                    "media_type": "video"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }
        finally:
            # Always clean up
            if audio_path.exists():
                try:
                    audio_path.unlink()
                except:
                    pass
    
    def _process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text from PDF"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            # Try PyMuPDF first
            try:
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
            except:
                # Fallback to pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
            
            return {
                "media_type": "pdf",
                "chunks": [{
                    "text": text.strip(),
                    "timestamp": None,
                    "media_type": "pdf"
                }],
                "visual_forensics": {"suspicion_level": "none"}
            }
            
        except Exception as e:
            logger.error(f"PDF processing failed: {e}")
            return {
                "media_type": "pdf",
                "chunks": [{
                    "text": f"Failed to process PDF: {str(e)}",
                    "timestamp": None,
                    "media_type": "pdf"
                }],
                "visual_forensics": {"suspicion_level": "unknown"}
            }


if __name__ == "__main__":
    # Test
    agent = IngestionAgent()
    
    # Test text
    result = agent.ingest("This is a test claim", "text")
    print(f"Text result: {result}")
