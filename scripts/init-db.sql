-- PostgreSQL initialization script
-- This runs automatically when the database is first created

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For composite indexes

-- Create a read-only user for reporting/analytics (optional)
-- CREATE USER finalytics_readonly WITH PASSWORD 'readonly_password';
-- GRANT CONNECT ON DATABASE finalytics TO finalytics_readonly;
-- GRANT USAGE ON SCHEMA public TO finalytics_readonly;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO finalytics_readonly;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO finalytics_readonly;

-- Performance settings
ALTER DATABASE finalytics SET timezone TO 'UTC';
ALTER DATABASE finalytics SET client_encoding TO 'UTF8';
ALTER DATABASE finalytics SET default_transaction_isolation TO 'read committed';
ALTER DATABASE finalytics SET statement_timeout TO '30s';

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Finalytics database initialized successfully';
END $$;

