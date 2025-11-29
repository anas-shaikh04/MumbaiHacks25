# Veritas Guardian API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for demo version.

---

## Endpoints

### 1. Health Check

**GET** `/`

Check if API is running.

**Response:**
```json
{
  "status": "online",
  "service": "Veritas Guardian API",
  "version": "1.0.0"
}
```

---

### 2. Verify Text

**POST** `/api/verify/text`

Verify text content for misinformation.

**Request Body:**
```json
{
  "text": "5G towers cause COVID-19",
  "views": 10000,
  "likes": 500,
  "shares": 100,
  "comments": 50
}
```

**Parameters:**
- `text` (required): Text content to verify
- `views` (optional): Number of views/impressions
- `likes` (optional): Number of likes
- `shares` (optional): Number of shares
- `comments` (optional): Number of comments

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/verify/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Breaking news: 5G towers spreading coronavirus",
    "views": 50000,
    "likes": 2000
  }'
```

---

### 3. Verify URL

**POST** `/api/verify/url`

Verify content from a URL (news article or YouTube video).

**Request (Form Data):**
- `url`: URL to verify

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "pending"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/verify/url" \
  -F "url=https://www.youtube.com/watch?v=example"
```

---

### 4. Verify Image

**POST** `/api/verify/image`

Extract text from image and verify claims.

**Request (Multipart Form):**
- `file`: Image file (PNG, JPG, JPEG)

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "pending"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/verify/image" \
  -F "file=@screenshot.jpg"
```

---

### 5. Verify Video

**POST** `/api/verify/video`

Transcribe video audio and verify claims.

**Request (Multipart Form):**
- `file`: Video file (MP4, AVI, MOV, MKV)

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440003",
  "status": "pending"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/verify/video" \
  -F "file=@video.mp4"
```

---

### 6. Verify PDF

**POST** `/api/verify/pdf`

Extract text from PDF and verify claims.

**Request (Multipart Form):**
- `file`: PDF file

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440004",
  "status": "pending"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/verify/pdf" \
  -F "file=@document.pdf"
```

---

### 7. Get Result

**GET** `/api/result/{job_id}`

Get verification results for a completed job.

**Parameters:**
- `job_id`: Job ID from verification request

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": null,
  "result": {
    "primary_language": "en",
    "language_name": "English",
    "language_support": "full",
    "results": [
      {
        "claim_id": "clm_001",
        "claim": "5G towers cause COVID-19",
        "user_label": "False",
        "confidence": 95,
        "short_explain_en": "This claim has been debunked by WHO and health authorities.",
        "short_explain_local": "This claim has been debunked by WHO and health authorities.",
        "virality_score": 82,
        "combined_risk_level": "critical",
        "evidence": [
          {
            "url": "https://www.who.int/...",
            "title": "WHO debunks 5G coronavirus myth",
            "source_type": "health_authority",
            "credibility_score": 100
          }
        ],
        "receipt_pdf_path": "receipts/clm_001.pdf",
        "timestamp": "2025-11-25T10:30:00"
      }
    ],
    "visual_forensics": {
      "suspicion_level": "none"
    },
    "summary": {
      "total_claims": 1,
      "true_count": 0,
      "false_count": 1,
      "neutral_count": 0,
      "highest_risk": "critical"
    }
  },
  "error": null
}
```

**Status Values:**
- `pending`: Job queued
- `processing`: Currently being processed
- `completed`: Verification complete
- `failed`: Processing failed

**Example cURL:**
```bash
curl "http://localhost:8000/api/result/550e8400-e29b-41d4-a716-446655440000"
```

---

### 8. Get Progress

**GET** `/api/progress/{job_id}`

Poll for job progress (lighter than full result).

**Parameters:**
- `job_id`: Job ID

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": "Starting pipeline..."
}
```

**Example cURL:**
```bash
curl "http://localhost:8000/api/progress/550e8400-e29b-41d4-a716-446655440000"
```

---

### 9. Download Receipt

**GET** `/api/download/{job_id}/{claim_id}`

Download PDF verification receipt.

**Parameters:**
- `job_id`: Job ID
- `claim_id`: Claim ID (e.g., "clm_001")

**Response:**
PDF file download

**Example:**
```
http://localhost:8000/api/download/550e8400-e29b-41d4-a716-446655440000/clm_001
```

---

### 10. Get Workflow

**GET** `/api/workflow/{job_id}`

Get agent workflow for transparency.

**Parameters:**
- `job_id`: Job ID

**Response:**
```json
{
  "workflow": [
    {
      "agent": "Agent 1 - Ingestion",
      "action": "Extracted text and performed visual forensics",
      "status": "complete"
    },
    {
      "agent": "Agent 2 - Claims",
      "action": "Detected language and extracted 1 claims",
      "status": "complete"
    }
  ],
  "timestamp": "2025-11-25T10:30:00"
}
```

---

### 11. Delete Job

**DELETE** `/api/job/{job_id}`

Remove job from memory.

**Parameters:**
- `job_id`: Job ID

**Response:**
```json
{
  "status": "deleted",
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Result Schema

### Claim Result Object
```json
{
  "claim_id": "clm_001",
  "claim": "Canonical claim text",
  "original_text": "Original text snippet",
  "language": "en",
  "user_label": "True" | "False" | "Neutral",
  "confidence": 95,
  "short_explain_en": "English explanation",
  "short_explain_local": "Local language explanation",
  "needs_human_review": false,
  "evidence": [...],
  "internal_label": "Supported",
  "virality_score": 75,
  "reach_score": 60,
  "engagement_score": 45,
  "content_boost_score": 1.5,
  "combined_risk_level": "high",
  "receipt_pdf_path": "receipts/clm_001.pdf",
  "timestamp": "2025-11-25T10:30:00"
}
```

### Evidence Object
```json
{
  "url": "https://example.com/article",
  "title": "Article title",
  "snippet": "Excerpt from article...",
  "source_type": "govt" | "health_authority" | "factcheck" | "news" | "other",
  "credibility_score": 85
}
```

### Risk Levels
- `low`: Low risk, mostly true or low virality
- `medium`: Moderate risk, neutral claims or moderate spread
- `high`: High risk, false claims with medium spread
- `critical`: Critical risk, false claims with high virality

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Job not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Job not completed"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limiting

No rate limiting in demo version. For production:
- Implement rate limiting per IP
- Use Redis for job storage
- Add authentication tokens

---

## Typical Workflow

1. **Submit verification request**
   ```
   POST /api/verify/text → {job_id}
   ```

2. **Poll for completion**
   ```
   GET /api/progress/{job_id} → {status}
   ```

3. **Get results**
   ```
   GET /api/result/{job_id} → {result}
   ```

4. **Download receipt (optional)**
   ```
   GET /api/download/{job_id}/{claim_id} → PDF
   ```

5. **View workflow (optional)**
   ```
   GET /api/workflow/{job_id} → {workflow}
   ```

---

## Python Client Example

```python
import requests
import time

# Submit verification
response = requests.post(
    "http://localhost:8000/api/verify/text",
    json={
        "text": "5G towers cause COVID-19",
        "views": 10000
    }
)
job_id = response.json()["job_id"]

# Poll until complete
while True:
    progress = requests.get(f"http://localhost:8000/api/progress/{job_id}")
    status = progress.json()["status"]
    
    if status == "completed":
        break
    elif status == "failed":
        raise Exception("Verification failed")
    
    time.sleep(2)

# Get results
result = requests.get(f"http://localhost:8000/api/result/{job_id}")
print(result.json())
```

---

## Notes

- Processing time varies by input type (text: 5-10s, video: 30-60s)
- Jobs are stored in memory (cleared on restart)
- PDF receipts stored in `receipts/` directory
- Temporary uploads stored in `temp/uploads/`

---

## Production Recommendations

1. Add authentication (API keys, OAuth)
2. Implement rate limiting
3. Use Redis/PostgreSQL for job storage
4. Add request validation
5. Implement HTTPS
6. Add monitoring/logging
7. Set up CORS properly
8. Add backup for receipts
9. Implement job expiration
10. Add webhook notifications
