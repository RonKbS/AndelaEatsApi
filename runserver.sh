#!/bin/sh

flask db init
flask db migrate
flask db upgrade

GUNICORN_WORKERS=2

gunicorn "andelaeats.app:create_app()" -b :4070 -w $GUNICORN_WORKERS -k gevent --max-requests=5000 --max-requests-jitter=500 --timeout=360 --reload
