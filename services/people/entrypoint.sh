#!/bin/sh

echo "Waiting for mongodb..."

while ! nc -z db 27017; do echo sleeping; sleep 0.1; done

echo "mongodb started"

python manage.py run -h 0.0.0.0