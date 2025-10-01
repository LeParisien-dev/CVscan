from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
import src.api.health as health
import src.api.upload as upload
import src.api.job as job
import src.api.match as match
import src.api.ai_routes as ai

app = FastAPI(title="CVscan API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(job.router, prefix="/api/v1")
app.include_router(match.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
