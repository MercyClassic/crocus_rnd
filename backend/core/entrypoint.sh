#!/bin/bash
cd /market/backend/core/src
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 config.wsgi
