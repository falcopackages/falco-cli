#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py makesuperuser
gunicorn config.wsgi --config="deploy/gunicorn.conf.py"
