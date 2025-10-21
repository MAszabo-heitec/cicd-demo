# Többlépcsős (multi‑stage) Docker build a kisebb image‑méret és biztonság érdekében

## 1. lépés: base stage – függőségek telepítése
FROM python:3.11-slim AS builder
WORKDIR /app
# Frissítések és szükséges csomagok
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*
# Másoljuk a függőségek listáját és telepítsük
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

## 2. lépés: final stage – csak a futtatáshoz szükséges állományok
FROM python:3.11-slim
WORKDIR /app
# A builder stage‑ből bemásoljuk a telepített Python környezetet
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/share /usr/local/share

# Alkalmazás kód bemásolása
COPY app/ ./app/

# Build arguments to define application version and environment. Provide defaults
# but allow overriding at build time using `--build-arg APP_VERSION=...` and
# `--build-arg ENVIRONMENT=...`. These values become environment variables
# within the container and are used by the /info endpoint.
ARG APP_VERSION=1.0.0
ARG ENVIRONMENT=production
ENV APP_VERSION=$APP_VERSION
ENV ENVIRONMENT=$ENVIRONMENT

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

CMD ["python", "app/main.py"]