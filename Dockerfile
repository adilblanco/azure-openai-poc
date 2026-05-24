# ================================================================
# Dockerfile — azure-openai-poc
# ================================================================
FROM python:3.10-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app"

WORKDIR /app

# ---------------------------------------------------------------
# Étape 1 : Dépendances système
# ---------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ \
    curl ca-certificates \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------
# Étape 2 : Dépendances Python
# ---------------------------------------------------------------
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install --no-cache-dir gunicorn && \
    rm -rf /root/.cache/pip

# ---------------------------------------------------------------
# Étape 3 : Code applicatif
# ---------------------------------------------------------------
COPY . /app

# ---------------------------------------------------------------
# Étape 4 : Port et démarrage
# ---------------------------------------------------------------
EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers=2", "--threads=4", "--timeout=90"]
