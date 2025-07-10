-- Enable pgvector extension (must be run as superuser)
CREATE EXTENSION IF NOT EXISTS vector;

-- -- Create your app user
-- CREATE USER myuser WITH PASSWORD 'supersecret';

-- -- Grant database privileges
-- GRANT ALL PRIVILEGES ON DATABASE rag_db TO myuser;

-- -- Grant usage and create privileges on schema
-- GRANT USAGE, CREATE ON SCHEMA public TO myuser;


-- You can pre-create your tables here if you want.
-- This helps ensure they exist before the app starts.
-- Otherwise, SQLAlchemy/Alembic will handle this.

-- Example Table (will be managed by Alembic later)
-- CREATE TABLE IF NOT EXISTS users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- );