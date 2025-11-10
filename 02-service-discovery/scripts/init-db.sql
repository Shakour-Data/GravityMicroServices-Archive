-- ===================================
-- Service Discovery Database Initialization
-- ===================================
-- This script initializes the PostgreSQL database for Service Discovery service
-- It creates the database, user, and necessary extensions

-- Create database (if using postgres user)
-- SELECT 'CREATE DATABASE service_discovery_db'
-- WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'service_discovery_db')\gexec

-- Connect to database
\c service_discovery_db;

-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- Better indexing

-- Create schema for service discovery
CREATE SCHEMA IF NOT EXISTS service_registry;

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA service_registry TO sd_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO sd_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA service_registry GRANT ALL ON TABLES TO sd_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA service_registry GRANT ALL ON SEQUENCES TO sd_user;

-- Create service_instances table (will be created by SQLAlchemy, but we can prepare)
-- This is optional - SQLAlchemy will create tables via Alembic migrations

-- Indexes for better query performance (will be created by migrations)
-- CREATE INDEX IF NOT EXISTS idx_service_name ON service_registry.service_instances(service_name);
-- CREATE INDEX IF NOT EXISTS idx_service_status ON service_registry.service_instances(status);
-- CREATE INDEX IF NOT EXISTS idx_last_heartbeat ON service_registry.service_instances(last_heartbeat);

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Service Discovery database initialized successfully!';
    RAISE NOTICE '📊 Database: service_discovery_db';
    RAISE NOTICE '👤 User: sd_user';
    RAISE NOTICE '🔧 Extensions: uuid-ossp, pg_trgm, btree_gin';
END $$;
