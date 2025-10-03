from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json

from src.services.langchain_service import compute_similarity

router = APIRouter()
UPLOAD_DIR = Path("uploads")
JOBS_DIR = Path("jobs")

class MatchRequest(BaseModel):
    cv_filename: str
    job_id: str

@router.post("/match")
def match_cv_to_job(request: MatchRequest):
    """Match an uploaded CV to a stored job description and return similarity score."""
    cv_path = UPLOAD_DIR / request.cv_filename
    job_path = JOBS_DIR / f"{request.job_id}.json"

    if not cv_path.exists():
        raise HTTPException(status_code=404, detail="CV not found")
    if not job_path.exists():
        raise HTTPException(status_code=404, detail="Job description not found")

    # Load CV text
    with open(cv_path, "r") as f:
        cv_text = f.read()

    # Load job description
    with open(job_path, "r") as f:
        job_data = json.load(f)

    job_text = job_data["description"]

    # Compute similarity score
    score = compute_similarity(cv_text, job_text)

    return {
        "status": "success",
        "cv": request.cv_filename,
        "job_id": request.job_id,
        "score": score,
        "message": f"Similarity between CV and job '{job_data['title']}' at {job_data['company']}"
    }
