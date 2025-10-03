EXECUTIVE SUMMARY
CVscan is an AI-powered resume analysis backend built with FastAPI. It accepts resume input (file or text), compares it to a job description, and returns structured insights (score, strengths, gaps, summary). The system is provider-agnostic (OpenRouter by default, OpenAI optional), production-ready for deployment on Render, and instrumented for safe usage with environment variables and test scripts.

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
- Python 3.12
- FastAPI
- Uvicorn
- httpx
- Pydantic
- python-multipart
- langchain-openai (for embeddings and similarity when needed)
- OpenRouter / OpenAI API

PROJECT STRUCTURE (relevant backend parts)
CVscan/
  apps/
    backend/
      src/
        api/          # API routers (health, upload, job, match, ai)
        core/         # Core configuration
        models/       # Data models and entities
        services/     # Business logic and external integrations
          llm/        # LLM providers and service switch
            llm_interface.py
            openai_provider.py
            openrouter_provider.py
            llm_service.py
        tests/        # Unit/integration tests
        utils/        # Helpers
  scripts/            # Utility scripts (curl tests, etc.)
  docs/               # Documentation and screenshots

ENVIRONMENT VARIABLES
Create a file apps/backend/.env with the following keys. Do not commit this file.

  # Provider
  LLM_PROVIDER=openrouter        # or: openai

  # OpenAI
  OPENAI_API_KEY=
  OPENAI_MODEL=gpt-5-mini

  # OpenRouter
  OPENROUTER_API_KEY=
  OPENROUTER_MODEL=openai/gpt-4.1-mini
  OPENROUTER_REFERRER=http://localhost:4000
  OPENROUTER_TITLE=CVscan

REQUIREMENTS
Ensure your requirements.txt contains pinned versions including, for example:
  fastapi==0.115.0
  uvicorn==0.30.6
  httpx==0.27.2
  pydantic==2.9.2
  python-multipart==0.0.20
  langchain-openai==0.2.3

(Adjust versions based on `pip show <package>` outputs on your system.)

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
  curl -X POST http://localhost:7000/api/v1/ai/analyze-cv     -H "Content-Type: application/json"     -d '{
      "text": "John Doe, 5 years in Python and FastAPI...",
      "job": "AI Engineer with NLP skills"
    }'

EXAMPLE RESPONSE (illustrative)
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
    curl -s https://api.openai.com/v1/chat/completions       -H "Authorization: Bearer $OPENAI_API_KEY"       -H "Content-Type: application/json"       -d "{
        \"model\": \"${OPENAI_MODEL:-gpt-5-mini}\",
        \"messages\": [{\"role\":\"user\",\"content\":\"$PROMPT\"}],
        \"max_tokens\": 32
      }"
  else
    if [ -z "$OPENROUTER_API_KEY" ]; then echo "OPENROUTER_API_KEY not set"; exit 1; fi
    curl -s https://openrouter.ai/api/v1/chat/completions       -H "Authorization: Bearer $OPENROUTER_API_KEY"       -H "Content-Type: application/json"       -H "HTTP-Referer: ${OPENROUTER_REFERRER:-http://localhost:4000}"       -H "X-Title: ${OPENROUTER_TITLE:-CVscan}"       -d "{
        \"model\": \"${OPENROUTER_MODEL:-openai/gpt-4.1-mini}\",
        \"messages\": [{\"role\":\"user\",\"content\":\"$PROMPT\"}],
        \"max_tokens\": 32
      }"
  fi

TESTING THE SCRIPT
From the repository root:
  chmod +x scripts/test_llm.sh
  ./scripts/test_llm.sh "Ping"

GIT BASICS
Create a .gitignore before the first commit (already recommended):
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

INITIAL COMMIT AND PUSH (if not already done)
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
- Configure environment variables in the dashboard (same keys as your local .env, without secrets in code).
- Monitor /api/v1/health for uptime checks (UptimeRobot).

OPERATIONAL SAFETY
- Keep max_tokens conservative (e.g., 512–800).
- Add request size guards (reject very large inputs).
- Cache identical requests (hash of resume + job) to avoid repeated LLM calls.
- Log and monitor calls count to prevent unexpected usage.

LICENSE
This project is distributed under the MIT License.
