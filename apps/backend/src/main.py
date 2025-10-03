import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers explicitly
import src.api.health as health
import src.api.upload as upload
import src.api.job as job
import src.api.match as match
import src.api.ai_routes as ai_routes

# Track app start time for uptime
START_TIME = time.time()

# App instance
app = FastAPI(
    title="CVScan API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS with env support
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(job.router, prefix="/api/v1")
app.include_router(match.router, prefix="/api/v1")
app.include_router(ai_routes.router, prefix="/api/v1")

# Root route (useful for recruiters visiting Render root URL)
@app.get("/")
def root():
    return {
        "message": "Welcome to CVScan API",
        "health": "/api/v1/health",
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }

# Entrypoint
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7000))  # Render provides PORT, default 7000 local
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
