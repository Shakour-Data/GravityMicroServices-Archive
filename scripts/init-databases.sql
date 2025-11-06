-- Initialize databases for all microservices
-- This script creates separate databases for each service

-- Service Discovery Database
CREATE DATABASE service_discovery;
GRANT ALL PRIVILEGES ON DATABASE service_discovery TO gravity;

-- Config Server Database
CREATE DATABASE config_server;
GRANT ALL PRIVILEGES ON DATABASE config_server TO gravity;

-- API Gateway Database
CREATE DATABASE api_gateway;
GRANT ALL PRIVILEGES ON DATABASE api_gateway TO gravity;

-- Auth Service Database
CREATE DATABASE auth_service;
GRANT ALL PRIVILEGES ON DATABASE auth_service TO gravity;

-- User Service Database
CREATE DATABASE user_service;
GRANT ALL PRIVILEGES ON DATABASE user_service TO gravity;

-- Notification Service Database
CREATE DATABASE notification_service;
GRANT ALL PRIVILEGES ON DATABASE notification_service TO gravity;

-- File Storage Service Database
CREATE DATABASE file_storage_service;
GRANT ALL PRIVILEGES ON DATABASE file_storage_service TO gravity;

-- Payment Service Database
CREATE DATABASE payment_service;
GRANT ALL PRIVILEGES ON DATABASE payment_service TO gravity;

-- Messaging Service Database
CREATE DATABASE messaging_service;
GRANT ALL PRIVILEGES ON DATABASE messaging_service TO gravity;

-- Analytics Service Database
CREATE DATABASE analytics_service;
GRANT ALL PRIVILEGES ON DATABASE analytics_service TO gravity;

-- Cache Service Database
CREATE DATABASE cache_service;
GRANT ALL PRIVILEGES ON DATABASE cache_service TO gravity;

-- Search Service Database
CREATE DATABASE search_service;
GRANT ALL PRIVILEGES ON DATABASE search_service TO gravity;

-- Email Service Database
CREATE DATABASE email_service;
GRANT ALL PRIVILEGES ON DATABASE email_service TO gravity;

-- SMS Service Database
CREATE DATABASE sms_service;
GRANT ALL PRIVILEGES ON DATABASE sms_service TO gravity;

-- Enable UUID extension for all databases
\c service_discovery;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c config_server;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c api_gateway;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c auth_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

\c user_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c notification_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c file_storage_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c payment_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c messaging_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c analytics_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c cache_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

\c search_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

\c email_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

\c sms_service;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
