# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# System deps (compilation + Postgres client headers + venv)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip toolchain
RUN python3 -m pip install --upgrade pip setuptools wheel

# Copy backend requirements (depuis le dossier backend)
COPY requirements.txt .

# Create venv and install deps inside
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Sanity check (fail build if an import is missing)
RUN /opt/venv/bin/python -c "import fastapi, sqlalchemy, pdfplumber, PyPDF2, langchain, langchain_openai, tiktoken; print('Deps OK')"


# ---------- Stage 2: runner ----------
FROM python:3.11-slim

WORKDIR /app

# Runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Bring the virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Always use the venv
ENV PATH="/opt/venv/bin:$PATH"
ENV ENV=docker
ENV PORT=7000
# Important: src est copié à /app/src, on le rend visible à Python
ENV PYTHONPATH=/app/src

# Non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup
USER appuser

# Copy ONLY backend code into the image
COPY . .

EXPOSE 7000

# Thanks to PYTHONPATH, "main:app" suffit (main.py est dans /app/src)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
