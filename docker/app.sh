#!/bin/bash

uv run alembic upgrade head

uv run gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000