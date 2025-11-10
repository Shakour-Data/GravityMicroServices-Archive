"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - User Service
File         : config.py
Description  : Configuration management using Pydantic Settings
Language     : English (UK)
Framework    : FastAPI / Python 3.11+

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Elena Volkov (Backend & Integration Lead)
Contributors      : Dr. Sarah Chen (Chief Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-08 08:00 UTC
Last Modified     : 2025-11-08 08:00 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-08 - Elena Volkov - Initial configuration

================================================================================
DEPENDENCIES
================================================================================
Internal  : None
External  : pydantic-settings, pydantic
Database  : PostgreSQL 16+, Redis 7

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/GravityWavesMl/user-service

================================================================================
"""

from typing import Annotated, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses Pydantic Settings for automatic validation and type conversion.
    Environment variables are loaded from .env file in development.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Gravity User Service"
    API_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "User Service API"
    API_DESCRIPTION: str = "User profile and preference management service"
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8082, description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes")
    
    # Database (PostgreSQL)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://user_service:password@localhost:5433/user_db",
        description="PostgreSQL connection URL"
    )
    DB_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Max overflow connections")
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/2",
        description="Redis connection URL"
    )
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Max Redis connections")
    REDIS_SESSION_TTL: int = Field(default=86400, description="Session TTL in seconds (24h)")
    REDIS_CACHE_TTL: int = Field(default=3600, description="Cache TTL in seconds (1h)")
    
    # Authentication
    AUTH_SERVICE_URL: str = Field(
        default="http://localhost:8081",
        description="Auth service URL"
    )
    JWT_SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    
    # File Service
    FILE_SERVICE_URL: str = Field(
        default="http://localhost:8084",
        description="File service URL for avatar uploads"
    )
    MAX_AVATAR_SIZE: int = Field(default=5242880, description="Max avatar size (5MB)")
    ALLOWED_AVATAR_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "image/webp"],
        description="Allowed avatar MIME types"
    )
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS origins"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow credentials")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list."""
        return self.CORS_ORIGINS
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = Field(default=20, description="Default page size")
    MAX_PAGE_SIZE: int = Field(default=100, description="Maximum page size")
    
    # Session Management
    MAX_ACTIVE_SESSIONS: int = Field(default=5, description="Max active sessions per user")
    SESSION_REFRESH_THRESHOLD: int = Field(
        default=3600,
        description="Refresh session if expires in less than 1 hour"
    )
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = Field(default=True, description="Enable Prometheus metrics")
    
    # Service Discovery
    SERVICE_DISCOVERY_URL: str = Field(
        default="http://localhost:8500",
        description="Service discovery URL"
    )
    SERVICE_ID: str = Field(default="user-service-1", description="Service instance ID")
    SERVICE_NAME: str = Field(default="user-service", description="Service name")
    
    # Logging
    JSON_LOGS: bool = Field(default=False, description="Use JSON format for logs")


# Create global settings instance
settings = Settings()
