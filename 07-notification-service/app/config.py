"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform - Notification Service
File         : config.py
Description  : Configuration management using Pydantic Settings
Language     : English (UK)
Framework    : FastAPI / Python 3.12.10

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : Elena Volkov (Database Architect)
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-09
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-09 - Dr. Sarah Chen - Initial configuration

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
================================================================================
"""

import sys
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Python version check - MUST be 3.12.10
REQUIRED_PYTHON = (3, 12, 10)
if sys.version_info[:3] != REQUIRED_PYTHON:
    raise RuntimeError(
        f"❌ Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}.{REQUIRED_PYTHON[2]} is required. "
        f"You are using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}. "
        f"Please install Python 3.12.10 and try again."
    )


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Notification Service configuration including:
    - SMTP for email
    - Twilio for SMS
    - Firebase for push notifications
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Gravity Notification Service"
    API_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    API_TITLE: str = "Notification Service API"
    API_DESCRIPTION: str = "Email, SMS, and Push notification service"
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8083, description="Server port")
    WORKERS: int = Field(default=4, description="Number of worker processes")
    
    # Database (PostgreSQL)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://notification_service:password@localhost:5433/notification_db",
        description="PostgreSQL connection URL"
    )
    DB_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=10, description="Max overflow connections")
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/3",
        description="Redis connection URL"
    )
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Max Redis connections")
    REDIS_CACHE_TTL: int = Field(default=3600, description="Cache TTL in seconds (1h)")
    
    # Authentication
    AUTH_SERVICE_URL: str = Field(
        default="http://localhost:8081",
        description="Auth service URL for token validation"
    )
    JWT_SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    
    # Email (SMTP)
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP server host")
    SMTP_PORT: int = Field(default=587, description="SMTP server port")
    SMTP_USERNAME: str = Field(default="", description="SMTP username")
    SMTP_PASSWORD: str = Field(default="", description="SMTP password")
    SMTP_FROM_EMAIL: str = Field(
        default="noreply@gravity.com",
        description="Default sender email"
    )
    SMTP_FROM_NAME: str = Field(
        default="Gravity Platform",
        description="Default sender name"
    )
    SMTP_USE_TLS: bool = Field(default=True, description="Use TLS for SMTP")
    SMTP_TIMEOUT: int = Field(default=10, description="SMTP timeout in seconds")
    
    # SMS (Twilio)
    TWILIO_ACCOUNT_SID: str = Field(default="", description="Twilio Account SID")
    TWILIO_AUTH_TOKEN: str = Field(default="", description="Twilio Auth Token")
    TWILIO_PHONE_NUMBER: str = Field(default="", description="Twilio phone number")
    TWILIO_WEBHOOK_URL: str = Field(
        default="",
        description="Webhook URL for Twilio callbacks"
    )
    TWILIO_ENABLED: bool = Field(default=False, description="Enable Twilio SMS")
    
    # Push Notifications (Firebase)
    FIREBASE_CREDENTIALS_PATH: str = Field(
        default="./config/firebase-credentials.json",
        description="Path to Firebase credentials JSON"
    )
    FIREBASE_PROJECT_ID: str = Field(default="", description="Firebase project ID")
    FIREBASE_ENABLED: bool = Field(default=False, description="Enable Firebase push")
    
    # APNs (Apple Push Notification Service)
    APNS_CERT_PATH: str = Field(
        default="./config/apns-cert.pem",
        description="Path to APNs certificate"
    )
    APNS_KEY_PATH: str = Field(
        default="./config/apns-key.pem",
        description="Path to APNs key"
    )
    APNS_ENABLED: bool = Field(default=False, description="Enable APNs")
    
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
    
    # Retry Logic
    MAX_RETRY_ATTEMPTS: int = Field(default=5, description="Max retry attempts")
    RETRY_DELAYS: List[int] = Field(
        default=[30, 60, 300, 900, 3600],
        description="Retry delays in seconds"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Max requests per minute per user"
    )
    EMAIL_RATE_LIMIT: int = Field(
        default=100,
        description="Max emails per hour per user"
    )
    SMS_RATE_LIMIT: int = Field(
        default=20,
        description="Max SMS per hour per user"
    )
    
    # Templates
    TEMPLATE_DIR: str = Field(
        default="templates",
        description="Template directory path"
    )
    DEFAULT_LANGUAGE: str = Field(default="en", description="Default language")
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = Field(default=True, description="Enable Prometheus metrics")
    
    # Service Discovery
    SERVICE_DISCOVERY_URL: str = Field(
        default="http://localhost:8500",
        description="Consul service discovery URL"
    )
    SERVICE_ID: str = Field(
        default="notification-service-1",
        description="Service instance ID"
    )
    SERVICE_NAME: str = Field(
        default="notification-service",
        description="Service name"
    )
    
    # Logging
    JSON_LOGS: bool = Field(default=False, description="Use JSON format for logs")
    
    # Celery (Background Tasks)
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/4",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/5",
        description="Celery result backend"
    )


# Create global settings instance
settings = Settings()
