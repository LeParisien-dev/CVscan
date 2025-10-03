from fastapi import APIRouter, Depends
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
    """Store a job description in the database."""
    job_id = str(uuid.uuid4())

    db_job = Job(
        job_id=job_id,
        title=job.title,
        company=job.company,
        description=job.description,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return {
        "status": "success",
        "job_id": db_job.job_id,
        "message": "Job description stored successfully"
    }
