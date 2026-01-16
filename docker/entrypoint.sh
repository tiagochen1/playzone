#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
echo "==> Compiling SCSS..."
python manage.py compile_scss || true

echo "==> Collect static..."
python manage.py collectstatic --noinput || true

python manage.py runserver 0.0.0.0:8000
