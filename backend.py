"""
FastAPI Backend for Veritas Guardian
Provides REST API endpoints for the verification system
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json
import asyncio

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from loguru import logger

from pipeline import VeritasGuardianPipeline

# Initialize FastAPI app
app = FastAPI(
    title="Veritas Guardian API",
    description="Multi-Agent Misinformation Verification System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pipeline = VeritasGuardianPipeline()

# Job storage (in-memory for demo; use Redis/DB in production)
jobs: Dict[str, Dict[str, Any]] = {}

# Temp directory for uploads
UPLOAD_DIR = Path("./temp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Pydantic models
class VerifyTextRequest(BaseModel):
    text: str
    views: Optional[int] = None
    likes: Optional[int] = None
    shares: Optional[int] = None
    comments: Optional[int] = None


class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Background task to process verification
async def process_verification(
    job_id: str,
    user_input: Any,
    input_type: str,
    metadata: Optional[Dict[str, Any]]
):
    """Background task to run verification pipeline"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = "Starting pipeline..."
        
        logger.info(f"Processing job {job_id}")
        
        # Run pipeline
        result = pipeline.process(user_input, input_type, metadata)
        
        # Update job
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


# API Endpoints

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "online",
        "service": "Veritas Guardian API",
        "version": "1.0.0"
    }


@app.post("/api/verify/text")
async def verify_text(
    request: VerifyTextRequest,
    background_tasks: BackgroundTasks
):
    """
    Verify text content
    
    Returns job_id to check status
    """
    job_id = str(uuid.uuid4())
    
    # Create job
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "input_type": "text"
    }
    
    # Prepare metadata
    metadata = {}
    if request.views:
        metadata["views"] = request.views
    if request.likes:
        metadata["likes"] = request.likes
    if request.shares:
        metadata["shares"] = request.shares
    if request.comments:
        metadata["comments"] = request.comments
    
    # Schedule background task
    background_tasks.add_task(
        process_verification,
        job_id,
        request.text,
        "text",
        metadata if metadata else None
    )
    
    return {"job_id": job_id, "status": "pending"}


@app.post("/api/verify/url")
async def verify_url(
    url: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    """Verify URL content"""
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "input_type": "url"
    }
    
    background_tasks.add_task(
        process_verification,
        job_id,
        url,
        "url",
        None
    )
    
    return {"job_id": job_id, "status": "pending"}


@app.post("/api/verify/image")
async def verify_image(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Verify image content"""
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "input_type": "image"
    }
    
    background_tasks.add_task(
        process_verification,
        job_id,
        str(file_path),
        "image",
        None
    )
    
    return {"job_id": job_id, "status": "pending"}


@app.post("/api/verify/video")
async def verify_video(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Verify video content"""
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "input_type": "video"
    }
    
    background_tasks.add_task(
        process_verification,
        job_id,
        str(file_path),
        "video",
        None
    )
    
    return {"job_id": job_id, "status": "pending"}


@app.post("/api/verify/pdf")
async def verify_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """Verify PDF content"""
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "input_type": "pdf"
    }
    
    background_tasks.add_task(
        process_verification,
        job_id,
        str(file_path),
        "pdf",
        None
    )
    
    return {"job_id": job_id, "status": "pending"}


@app.get("/api/job/{job_id}/status")
async def get_job_status(job_id: str):
    """Get status of a verification job (for polling)"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],

        progress=job.get("progress"),
        result=job.get("result"),
        error=job.get("error")
    )


@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    """Get verification result for a job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job.get("progress"),
        result=job.get("result"),
        error=job.get("error")
    )


@app.get("/api/progress/{job_id}")
async def get_progress(job_id: str):
    """Get progress status for a job (for polling)"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", "Processing...")
    }


@app.get("/api/download/{job_id}/{claim_id}")
async def download_receipt(job_id: str, claim_id: str):
    """Download PDF receipt for a specific claim"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    
    # Find claim
    result = job.get("result", {})
    for claim_result in result.get("results", []):
        if claim_result["claim_id"] == claim_id:
            pdf_path = claim_result.get("receipt_pdf_path")
            if pdf_path and os.path.exists(pdf_path):
                return FileResponse(
                    pdf_path,
                    media_type="application/pdf",
                    filename=f"verification_{claim_id}.pdf"
                )
    
    raise HTTPException(status_code=404, detail="Receipt not found")


@app.get("/api/workflow/{job_id}")
async def get_workflow(job_id: str):
    """Get agent workflow for transparency"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    
    result = job.get("result", {})
    workflow = pipeline.get_agent_workflow(result)
    
    return workflow


@app.delete("/api/job/{job_id}")
async def delete_job(job_id: str):
    """Delete a job from memory"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs[job_id]
    return {"status": "deleted", "job_id": job_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
