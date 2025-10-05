# ---------- Stage 1: builder ----------
FROM python:3.11-slim AS builder

# Set working directory inside the image
WORKDIR /app

# ---- System dependencies (for building psycopg2 and compiling extensions) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Upgrade Python toolchain ----
RUN python3 -m pip install --upgrade pip setuptools wheel

# ---- Install backend dependencies ----
COPY apps/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: runner ----------
FROM python:3.11-slim

# ---- Define base workdir ----
WORKDIR /app

# ---- Runtime dependencies (libpq for Postgres) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy installed dependencies from builder ----
COPY --from=builder /usr/local /usr/local

# ---- Copy backend code ----
COPY apps/backend ./apps/backend

# ---- Environment variables ----
ENV PORT=7000
ENV ENV=production
ENV PYTHONPATH=/app/apps/backend

# ---- Set working directory for runtime (Render fix) ----
WORKDIR /app/apps/backend

# ---- Expose port ----
EXPOSE 7000

# ---- Start FastAPI with Uvicorn ----
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7000"]
