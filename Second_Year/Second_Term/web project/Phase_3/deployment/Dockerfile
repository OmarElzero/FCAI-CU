# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=deployment.production_settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install psycopg2-binary gunicorn

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/deployment/static /app/deployment/media

# Collect static files
RUN python manage.py collectstatic --noinput --settings=deployment.production_settings

# Create a non-root user and change ownership
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run gunicorn
CMD gunicorn --bind 0.0.0.0:8000 --workers 3 jobsearch.wsgi:application
