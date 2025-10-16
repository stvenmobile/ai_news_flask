FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=America/New_York

RUN apt-get update && apt-get install -y --no-install-recommends \
      bash ca-certificates tzdata \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first so we can leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the app
COPY . /app

# Optional helper scripts (ignore if missing)
RUN chmod +x /app/refresh_news.sh /app/rebuild.sh || true

EXPOSE 8000

# Runs gunicorn against your Flask app object "app" in ai_news_flask_app.py
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:8000", "ai_news_flask_app:app"]
