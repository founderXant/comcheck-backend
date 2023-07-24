#!/usr/bin/env bash
# exit on error

python manage.py collectstatic --no-input
pip install -r requirements.txt