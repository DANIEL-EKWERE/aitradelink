##!/usr/bin/env bash
# exist on error

# set -o errexit

# pip install -r requirements.txt

# pip install gunicorn

# python manage.py collectstatic --no-input

# python manage.py migrate

#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install build dependencies
pip install --upgrade pip setuptools wheel

# Install requirements with binary preference for Pillow
pip install --only-binary=Pillow -r requirements.txt

# Install gunicorn (or add it to requirements.txt)
pip install gunicorn

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
