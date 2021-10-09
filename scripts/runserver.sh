#!/bin/bash

export DJANGO_DEBUG=True
export DJANGO_SECRET_KEY=$(cat ./scripts/key)
python3 manage.py runserver 8001 --noreload
