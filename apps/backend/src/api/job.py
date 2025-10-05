from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.job import Job
import uuid

router = APIRouter()

class JobDescription(BaseModel):
    title: str
    company: str
    description: str

@router.post("/job")
def create_job(job: JobDescription, db: Session = Depends(get_db)):
    """Store a job description directly in the PostgreSQL database."""
    job_id = str(uuid.uuid4())

    # Create a new Job record
    new_job = Job(
        job_id=job_id,
        title=job.title.strip(),
        company=job.company.strip(),
        description=job.description.strip(),
    )

    try:
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "status": "success",
        "job_id": new_job.job_id,
        "title": new_job.title,
        "company": new_job.company,
        "message": "Job description stored successfully in database"
    }
