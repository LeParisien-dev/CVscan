from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import uuid
import json

router = APIRouter()
JOBS_DIR = Path("jobs")
JOBS_DIR.mkdir(parents=True, exist_ok=True)

class JobDescription(BaseModel):
    title: str
    company: str
    description: str

@router.post("/job")
def create_job(job: JobDescription):
    """Store a job description locally as a JSON file."""
    job_id = str(uuid.uuid4())
    file_path = JOBS_DIR / f"{job_id}.json"

    with open(file_path, "w") as f:
        json.dump(job.dict(), f, indent=2)

    return {
        "status": "success",
        "job_id": job_id,
        "message": "Job description stored successfully"
    }
