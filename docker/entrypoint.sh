#!/bin/bash
chdir /market/src/
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 config.wsgi