#!/bin/bash

sleep 5

echo "BLAHHHHHHHHHHH"

python manage.py makemigrations

python manage.py migrate

python manage.py runscript db

python manage.py runsslserver 0.0.0.0:8000 --certificate certs/server.cert --key certs/server.key