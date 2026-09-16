FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
# Copy requirements
COPY backend/requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY backend/app ./app
COPY backend/alembic.ini .
# Run migrations and start server
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
