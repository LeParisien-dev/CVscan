# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# System deps (compilation + Postgres client headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip toolchain
RUN python3 -m pip install --upgrade pip setuptools wheel

# Copy backend requirements
COPY requirements.txt .

# Install deps globally (no need for custom venv)
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runner ----------
FROM python:3.11-slim

WORKDIR /app

# Runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy backend code
COPY . .

# Environment variables
ENV PORT=7000
ENV PYTHONPATH=/app/src

EXPOSE 7000

# Launch FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7000"]
