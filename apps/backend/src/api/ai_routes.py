from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm.llm_service import LlmService

router = APIRouter(prefix="/ai", tags=["AI"])

class AnalyzeRequest(BaseModel):
    text: str
    job: str | None = None

@router.post("/analyze-cv")
async def analyze_cv(req: AnalyzeRequest):
    llm = LlmService()
    prompt = (
        "You are a CV screening assistant.\n"
        "Return a JSON object {score:int, strengths:list, gaps:list, summary:str}.\n"
    )
    if req.job:
        prompt += f"\nJob description:\n{req.job}\n"
    prompt += f"\nCandidate CV:\n{req.text}"

    result = await llm.chat(
        prompt,
        system="Return ONLY JSON, no prose outside JSON.",
        max_tokens=600,
        temperature=0.2,
    )
    return result
