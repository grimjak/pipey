#!/bin/sh

echo "Waiting for mongodb..."

while ! nc -z people-db 27017; do echo sleeping; sleep 0.1; done

echo "mongodb started"

gunicorn -b 0.0.0.0:5000 manage:app