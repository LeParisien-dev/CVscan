from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.cv_document import CVDocument
from src.models.job import Job
from src.services.langchain_service import compute_similarity

router = APIRouter()

class MatchRequest(BaseModel):
    cv_filename: str
    job_id: str

@router.post("/match")
def match_cv_to_job(request: MatchRequest, db: Session = Depends(get_db)):
    """Compute similarity between a CV and a job stored in the database."""

    # 1️⃣ Fetch CV
    cv = db.query(CVDocument).filter(CVDocument.filename == request.cv_filename).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")

    # 2️⃣ Fetch job
    job = db.query(Job).filter(Job.job_id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    # 3️⃣ Compute similarity score
    try:
        score = compute_similarity(cv.content, job.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity computation failed: {str(e)}")

    # 4️⃣ Return result
    return {
        "status": "success",
        "cv_filename": cv.filename,
        "job_title": job.title,
        "company": job.company,
        "score": score,
        "message": f"Similarity between CV '{cv.filename}' and job '{job.title}' at {job.company}"
    }
