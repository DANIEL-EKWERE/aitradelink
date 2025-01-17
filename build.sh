#!/usr/bin/env bash
# exist on error

set -o errexit

pip install -r requirements.txt

pip install gunicorn

python manage.py collectstatic --no-input

python manage.py migrate