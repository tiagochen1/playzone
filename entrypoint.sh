#!/bin/sh
set -e

echo "==> Migrating database..."
python manage.py migrate --noinput

echo "==> Collect static..."
python manage.py collectstatic --noinput || true

echo "==> Compiling SCSS..."
python manage.py compile_scss || true

echo "==> Starting server..."
python manage.py runserver 0.0.0.0:8000
