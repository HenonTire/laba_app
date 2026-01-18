FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run server (fallback port if PORT is missing)
CMD ["sh", "-c", "gunicorn laba.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
