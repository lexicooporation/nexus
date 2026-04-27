#!/usr/bin/env bash
set -e

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear
python manage.py migrate
python manage.py createsuperuser --no-input 2>/dev/null || echo "Superuser already exists, skipping."