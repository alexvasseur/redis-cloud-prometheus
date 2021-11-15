#!/bin/bash

export FLASK_APP=app.py
export FLASK_DEBUG=1

# for use in Docker image
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# make sure logs are streamed to Docker stdout
export PYTHONUNBUFFERED=1

# unsecure bind on all iface for when running in Docker
pipenv run python -V
pipenv run python -m flask run -p 5000 --host 0.0.0.0


