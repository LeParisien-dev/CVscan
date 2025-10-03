CVscan

EXECUTIVE SUMMARY
CVscan is an AI-powered resume analysis backend built with FastAPI.
It accepts resume input (file or text), compares it to a job description, and returns structured insights (score, strengths, gaps, summary).

The system is provider-agnostic (OpenRouter by default, OpenAI optional), production-ready for deployment on Render, and instrumented for safe usage with environment variables and test scripts.

PROJECT GOALS
- Provide a clean, professional API for resume analysis and job matching.
- Keep costs under control by defaulting to OpenRouter; allow switching to OpenAI via environment variables.
- Maintain a modular structure for future extensions (vector search, embeddings, UI).
- Be deployable quickly (Render), observable (health endpoint), and easy to test locally.

FEATURES
- Upload and parse resumes via REST.
- Extract structured insights: score, strengths, gaps, summary.
- Compare resume text against a job description.
- Switchable LLM provider (OpenRouter / OpenAI) through environment variables.
- Health endpoints for uptime monitoring.

TECH STACK
Python 3.12
FastAPI
Uvicorn
httpx
Pydantic
python-multipart
langchain-openai (for embeddings and similarity when needed)
OpenRouter / OpenAI API

PROJECT STRUCTURE (relevant backend parts)
CVscan/
  apps/
    backend/
      src/
        api/          API routers (health, upload, job, match, ai)
        core/         Core configuration
        models/       Data models and entities
        services/     Business logic and external integrations
          llm/        LLM providers and service switch
            llm_interface.py
            openai_provider.py
            openrouter_provider.py
            llm_service.py
        tests/        Unit/integration tests
        utils/        Helpers
  scripts/            Utility scripts (curl tests, etc.)
  docs/               Documentation and screenshots

ENVIRONMENT VARIABLES
Create a file apps/backend/.env with the following keys. Do not commit this file. Use .env.example as a template.

LLM_PROVIDER=openrouter        # or: openai
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5-mini
OPENROUTER_API_KEY=
OPENROUTER_MODEL=openai/gpt-4.1-mini
OPENROUTER_REFERRER=http://localhost:4000
OPENROUTER_TITLE=CVscan

REQUIREMENTS
There are two requirements files:
- Root requirements.txt for general project dependencies and experiments.
- Backend apps/backend/requirements.txt for building and deploying the FastAPI backend in Docker/Render.

Example pinned versions in apps/backend/requirements.txt:
fastapi==0.115.0
uvicorn[standard]==0.30.6
httpx==0.27.2
pydantic==2.9.2
python-multipart==0.0.20
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.13.2
pdfplumber==0.10.2
PyPDF2==3.0.1
langchain>=0.3.7,<0.4.0
langchain-openai>=0.3.34,<0.4.0
tiktoken>=0.7.0,<0.8.0
numpy==1.26.4
pytest==8.3.3

RUNNING LOCALLY
From the backend directory:
cd CVscan/apps/backend
uvicorn src.main:app --reload --port 7000

Base URL:
http://localhost:7000/api/v1

ROUTER REGISTRATION
The FastAPI app includes ai_routes, so the AI endpoint is available under /api/v1/ai.

KEY ENDPOINTS
GET  /api/v1/health
POST /api/v1/upload-cv
POST /api/v1/job
POST /api/v1/match
POST /api/v1/ai/analyze-cv

EXAMPLE REQUEST (POST /api/v1/ai/analyze-cv)
curl -X POST http://localhost:7000/api/v1/ai/analyze-cv \
  -H "Content-Type: application/json" \
  -d '{
      "text": "John Doe, 5 years in Python and FastAPI...",
      "job": "AI Engineer with NLP skills"
    }'

Example response:
{
  "model": "openai/gpt-4.1-mini",
  "result": "{ \"score\": 78, \"strengths\": [\"Python\", \"FastAPI\"], \"gaps\": [\"NLP\"], \"summary\": \"Strong backend developer, needs more NLP expertise.\" }",
  "usage": {
    "promptTokens": 350,
    "completionTokens": 120,
    "totalTokens": 470
  }
}

SCRIPTS
File: scripts/test_llm.sh

#!/usr/bin/env bash
if [ -f "apps/backend/.env" ]; then
  set -a
  source apps/backend/.env
  set +a
fi

PROVIDER="${LLM_PROVIDER:-openrouter}"
PROMPT=${1:-"Hello from CVscan"}

if [ "$PROVIDER" = "openai" ]; then
  if [ -z "$OPENAI_API_KEY" ]; then echo "OPENAI_API_KEY not set"; exit 1; fi
  curl -s https://api.openai.com/v1/chat/completions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"${OPENAI_MODEL:-gpt-5-mini}\",
      \"messages\": [{\"role\":\"user\",\"content\":\"$PROMPT\"}],
      \"max_tokens\": 32
    }"
else
  if [ -z "$OPENROUTER_API_KEY" ]; then echo "OPENROUTER_API_KEY not set"; exit 1; fi
  curl -s https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -H "HTTP-Referer: ${OPENROUTER_REFERRER:-http://localhost:4000}" \
    -H "X-Title: ${OPENROUTER_TITLE:-CVscan}" \
    -d "{
      \"model\": \"${OPENROUTER_MODEL:-openai/gpt-4.1-mini}\",
      \"messages\": [{\"role\":\"user\",\"content\":\"$PROMPT\"}],
      \"max_tokens\": 32
    }"
fi

Run it:
chmod +x scripts/test_llm.sh
./scripts/test_llm.sh "Ping"

GIT BASICS
Create a .gitignore before the first commit (already added):

__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
.venv/
env/
venv/
*.log
.vscode/
.idea/
*.env
.DS_Store

INITIAL COMMIT AND PUSH
git init
git add .
git commit -m "Initial commit: CVscan backend, providers, scripts, docs"
git branch -M main
git remote add origin git@github.com:LeParisien-dev/CVscan.git
git push -u origin main

DEPLOYMENT (RENDER EXAMPLE)
- Create a new Web Service from your GitHub repository.
- Set the start command:
  uvicorn src.main:app --host 0.0.0.0 --port 7000
- Expose port 7000.
- Configure environment variables in the Render dashboard (use the same keys as .env, but never commit secrets).
- Monitor /api/v1/health for uptime checks (UptimeRobot).

OPERATIONAL SAFETY
- Keep max_tokens conservative (e.g., 512–800).
- Add request size guards (reject very large inputs).
- Cache identical requests (resume + job hash) to avoid repeated LLM calls.
- Log and monitor usage to prevent unexpected costs.

LICENSE
This project is distributed under the MIT License.
