#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py makesuperuser
granian --interface wsgi config.wsgi:application --host 0.0.0.0 --port 80 --workers 4
