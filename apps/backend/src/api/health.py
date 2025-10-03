from fastapi import APIRouter
import time
from datetime import datetime

router = APIRouter()
START_TIME = time.time()

@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "message": "CVScan backend is running",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/ping")
def get_ping():
    return {"status": "ok"}
