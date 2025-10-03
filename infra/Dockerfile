# Builder stage
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runner stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY apps/backend ./apps/backend

ENV PATH=/root/.local/bin:$PATH
ENV PORT=7000

EXPOSE 7000

CMD ["python", "apps/backend/main.py"]
