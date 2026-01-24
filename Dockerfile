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
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "laba.asgi:application"]
