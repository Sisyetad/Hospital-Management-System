#!/bin/sh
set -e

echo "⏳ Waiting for PostgreSQL..."
while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  sleep 1
done
echo "✅ PostgreSQL is ready."

echo "🔄 Running migrations..."
python manage.py migrate

echo "👤 Creating superuser..."
python manage.py create_superuser
echo "✅ Superuser check complete."

echo "🚀 Starting Gunicorn..."
gunicorn medicalschedulerbackend.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
