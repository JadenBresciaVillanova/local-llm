# # Use an official Python runtime as a parent image
# FROM python:3.10-slim as builder

# # Set the working directory
# WORKDIR /app

# # Install poetry (or just use pip)
# RUN pip install poetry

# # Copy only the dependency definition files
# COPY pyproject.toml poetry.lock ./

# # Install dependencies
# RUN poetry install --no-root --no-dev

# # --- Final Stage ---
# FROM python:3.10-slim

# WORKDIR /app

# # Copy the virtual environment from the builder stage
# COPY --from=builder /app/.venv /.venv

# # Activate the virtual environment
# ENV PATH="/app/.venv/bin:$PATH"

# # Copy the application code
# COPY . .

# # Command to run the app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# # --- Builder stage ---
# FROM python:3.10-slim as builder

# WORKDIR /app

# # Install Poetry and dependencies
# RUN pip install poetry

# COPY pyproject.toml poetry.lock ./
# RUN poetry install --no-root

# # --- Final stage ---
# FROM python:3.10-slim

# WORKDIR /app

# # Copy virtual env from builder
# COPY --from=builder /root/.cache/pypoetry/virtualenvs /root/.cache/pypoetry/virtualenvs
# ENV PATH="/root/.cache/pypoetry/virtualenvs/your_venv_name/bin:$PATH"

# # Install alembic and asyncpg here in the final image to be sure they are present
# RUN pip install alembic asyncpg pgvector

# COPY . .


# WORKDIR /app/backend

# # Copy Alembic configuration
# COPY backend/alembic /app/backend/alembic
# COPY backend/alembic.ini /app/backend/alembic.ini

# # Copy entrypoint script
# COPY entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh

# # Set entrypoint
# ENTRYPOINT ["/app/entrypoint.sh"]

# # Default command to run your app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Builder Stage ---
# --- Builder Stage ---
FROM python:3.10-slim as builder
WORKDIR /app
RUN pip install poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# This COPY command is correct because we moved pyproject.toml to the root
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root 

# --- Final Stage ---
FROM python:3.10-slim
WORKDIR /app

# Copy the virtual environment
COPY --from=builder /app/.venv ./.venv

# Copy ONLY the application code.
# The compose file will mount the config files.
COPY ./backend ./backend

# Copy and set permissions for the entrypoint script
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]