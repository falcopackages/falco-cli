#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi --config="deploy/gunicorn.conf.py"
