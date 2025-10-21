# syntax=docker/dockerfile:1

# Build stage: install dependencies into a minimal image
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --user --no-cache-dir -r requirements.txt

# Final stage: copy only what we need
FROM python:3.11-slim

LABEL org.opencontainers.image.title="Complex CI/CD Demo"
LABEL org.opencontainers.image.source="https://github.com/<USER>/<REPO>"

WORKDIR /app

ENV PATH="/root/.local/bin:${PATH}"

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/

EXPOSE 5000

ENV PORT=5000

CMD ["python", "-m", "app.main"]