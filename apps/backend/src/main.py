import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers explicitly (no need to populate __init__.py)
import src.api.health as health
import src.api.upload as upload
import src.api.job as job
import src.api.match as match
import src.api.ai_routes as ai_routes

# App instance
app = FastAPI(
    title="CVScan API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
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

# Entrypoint
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7000))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
