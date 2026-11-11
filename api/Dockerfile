# API image. Build from the repository root:
#   docker build -f api/Dockerfile -t tastelens-api .
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Dependencies first, so code changes do not reinstall them.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY recommender/ recommender/
COPY api/ api/

# Run as a non-root user; artifacts/ is where the model and data are stored.
RUN useradd --create-home appuser && mkdir -p artifacts && chown appuser artifacts
USER appuser

EXPOSE 8000
# Shell form so $PORT (set by hosts such as Render) is expanded.
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT}
