#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    uv run celery --app=app.tasks.celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    uv run celery --app=app.tasks.celery:celery flower
fi