import os
import time
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

# --- Routers imports ---
import src.api.health as health
import src.api.upload as upload
import src.api.job as job
import src.api.match as match
import src.api.match_stat as match_stat
import src.api.ai_routes as ai_routes
import src.api.auth as auth

# Track start time (for uptime endpoint)
START_TIME = time.time()

# --- FastAPI App ---
app = FastAPI(
    title="CVScan API",
    version="1.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    description=(
        "Backend service for CVScan — AI-driven CV/job matching platform.\n"
        "Includes both experimental LLM routes and statistical AI-Lite routes."
    )
)

# --- CORS setup ---
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers registration ---
app.include_router(health.router, prefix="/api/v1", tags=["system"])
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(job.router, prefix="/api/v1", tags=["job"])
app.include_router(match.router, prefix="/api/v1", tags=["match-legacy"])
app.include_router(match_stat.router, prefix="/api/v1", tags=["match-stat"])  # ✅ NEW
app.include_router(ai_routes.router, prefix="/api/v1", tags=["ai"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])

# --- Health endpoint (GET + HEAD) ---
@app.api_route("/api/v1/health", methods=["GET", "HEAD"], include_in_schema=False)
async def health_check():
    return JSONResponse(
        content={
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": round(time.time() - START_TIME, 2),
        }
    )

# --- Root endpoint (for Render root URL) ---
@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "Welcome to CVScan API",
        "docs": "/api/docs",
        "health": "/api/v1/health",
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }

# --- Entrypoint (for local dev) ---
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 7000))  # Render auto-provides PORT, default 7000 locally
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
