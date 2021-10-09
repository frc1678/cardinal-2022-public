#!/bin/bash

export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY=$(cat ./scripts/key)
python3 manage.py runserver 8001
