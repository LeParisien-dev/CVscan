# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# System deps (compilation + Postgres client headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools wheel

COPY apps/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runner ----------
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local
COPY apps/backend ./apps/backend


ENV PYTHONPATH=/app/apps/backend

EXPOSE 7000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7000"]
