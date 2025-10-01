from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "message": "CVscan backend is running",
    }
