-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- You can pre-create your tables here if you want.
-- This helps ensure they exist before the app starts.
-- Otherwise, SQLAlchemy/Alembic will handle this.

-- Example Table (will be managed by Alembic later)
-- CREATE TABLE IF NOT EXISTS users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );