#!/usr/bin/env bash

mkdir -p /tmp/logs

gunicorn -w 2 -b 0.0.0.0:8000 --access-logfile /tmp/logs/access.log mp.wsgi:application
