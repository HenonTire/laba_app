FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps only
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run collectstatic at runtime + start server
CMD python manage.py collectstatic --noinput && \
    gunicorn laba.wsgi:application --bind 0.0.0.0:$PORT
