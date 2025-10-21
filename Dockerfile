# Többlépcsős (multi-stage) Docker build a kisebb image-méret és biztonság érdekében.

# 1. lépés: builder stage – függőségek telepítése
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 2. lépés: végső stage – minimal runtime image
FROM python:3.11-slim
WORKDIR /app

# Másoljuk a telepített Python környezetet a builderből
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/share /usr/local/share

# Alkalmazás kód bemásolása
COPY app/ ./app/

# Build argumentumok a verzió és környezet beállításához (nem kötelező megadni)
ARG APP_VERSION=1.0.0
ARG ENVIRONMENT=production
ENV APP_VERSION=$APP_VERSION
ENV ENVIRONMENT=$ENVIRONMENT

ENV PYTHONUNBUFFERED=1
EXPOSE 5000

CMD ["python", "app/main.py"]