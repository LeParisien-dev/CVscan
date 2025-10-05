# Description: FastAPI route for AI-Lite statistical matching (no LLM)
# Endpoint: POST /api/v1/match-stat
# Body: { "cv_filename": "...", "job_id": "..." }
# Response: { "score": float, "details": { ... } }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.match_stat_service import match_stat

router = APIRouter()

class MatchStatRequest(BaseModel):
    cv_filename: str
    job_id: str

@router.post("/match-stat")
def match_stat_endpoint(payload: MatchStatRequest):
    """
    Compute statistical match score between a CV and a job.
    """
    try:
        result = match_stat(payload.cv_filename, payload.job_id)
        # result already has {"score": .., "details": {...}}
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        # Avoid leaking internals; send concise message
        raise HTTPException(status_code=500, detail=f"Internal error: {e.__class__.__name__}")
