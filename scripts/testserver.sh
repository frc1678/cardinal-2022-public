#!/bin/bash

export DJANGO_DEBUG=True
export DJANGO_SECRET_KEY=32498dsfdsklfj498wefksdlf894
python3 manage.py runserver 8001 --noreload
