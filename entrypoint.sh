#!/bin/sh
set -e

# Define the absolute path to the python executables in our venv
VENV_BIN="/app/.venv/bin"

echo "Waiting for postgres..."
# docker-compose healthcheck handles the actual waiting
echo "PostgreSQL started"

# Run database migrations using the absolute path to alembic
echo "Running database migrations..."
$VENV_BIN/alembic upgrade head

# Execute the main command (the CMD from Dockerfile) using its absolute path
# The "$@" represents the CMD from your Dockerfile: ["uvicorn", "backend.main:app", ...]
echo "Starting application..."
exec $VENV_BIN/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000