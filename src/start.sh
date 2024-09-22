#!/bin/bash
cd /app
python wait_for_postgres.py
alembic upgrade head
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
