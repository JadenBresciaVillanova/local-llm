# Use an official Python runtime as a parent image
FROM python:3.10-slim as builder

# Set the working directory
WORKDIR /app

# Install poetry (or just use pip)
RUN pip install poetry

# Copy only the dependency definition files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root --no-dev

# --- Final Stage ---
FROM python:3.10-slim

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /.venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY . .

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]