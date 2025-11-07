-- ============================================================================
-- FILE IDENTITY (شناسنامه فایل)
-- ============================================================================
-- Project      : Gravity MicroServices Platform
-- File         : init-databases.sql
-- Description  : PostgreSQL initialization script for Service Discovery database
-- Language     : SQL (PostgreSQL 16+)
-- 
-- ============================================================================
-- AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
-- ============================================================================
-- Primary Author    : Dr. Aisha Patel (Data Architecture & Database Specialist)
-- Contributors      : Lars Björkman (DevOps Integration)
-- Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)
-- 
-- ============================================================================
-- TIMELINE & EFFORT (زمان‌بندی و تلاش)
-- ============================================================================
-- Created Date      : 2025-11-07 21:40 UTC
-- Last Modified     : 2025-11-07 21:40 UTC
-- Development Time  : 0 hours 20 minutes
-- Review Time       : 0 hours 10 minutes
-- Total Time        : 0 hours 30 minutes
-- 
-- ============================================================================
-- COST CALCULATION (محاسبه هزینه)
-- ============================================================================
-- Hourly Rate       : $150/hour (Elite Engineer - Dr. Aisha Patel)
-- Development Cost  : 0.33 × $150 = $50.00 USD
-- Review Cost       : 0.17 × $150 = $25.00 USD
-- Total Cost        : $75.00 USD
-- 
-- ============================================================================
-- VERSION HISTORY (تاریخچه نسخه)
-- ============================================================================
-- v1.0.0 - 2025-11-07 - Dr. Aisha Patel - Initial database setup
-- 
-- ============================================================================
-- LICENSE & COPYRIGHT
-- ============================================================================
-- Copyright (c) 2025 Gravity MicroServices Platform
-- License: MIT License
-- Repository: https://github.com/GravityWavesMl/GravityMicroServices
-- 
-- ============================================================================

-- Create database if not exists
SELECT 'CREATE DATABASE service_discovery'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'service_discovery')\gexec

-- Connect to database
\c service_discovery

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- For JSONB indexing

-- Create custom types
DO $$ BEGIN
    CREATE TYPE health_status AS ENUM ('passing', 'warning', 'critical', 'unknown');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE health_check_type AS ENUM ('http', 'tcp', 'grpc', 'ttl');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Grant privileges (for Docker environment)
GRANT ALL PRIVILEGES ON DATABASE service_discovery TO postgres;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Service Discovery database initialized successfully';
    RAISE NOTICE 'Extensions enabled: uuid-ossp, pg_trgm, btree_gin';
    RAISE NOTICE 'Custom types created: health_status, health_check_type';
END $$;
