#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input --clear

gunicorn cars.wsgi:application --bind 0.0.0.0:$PORT

exec "$@"