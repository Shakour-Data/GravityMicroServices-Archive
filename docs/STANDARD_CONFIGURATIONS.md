# 🔧 STANDARD CONFIGURATIONS FOR ALL SERVICES

> **Complete configuration templates and standards for all 52 microservices**

**Version:** 1.0.0  
**Last Updated:** November 10, 2025

---

## 📑 TABLE OF CONTENTS

1. [Environment Configuration](#environment-configuration)
2. [Application Configuration](#application-configuration)
3. [Database Configuration](#database-configuration)
4. [Redis Configuration](#redis-configuration)
5. [Security Configuration](#security-configuration)
6. [Logging Configuration](#logging-configuration)
7. [Docker Configuration](#docker-configuration)
8. [Kubernetes Configuration](#kubernetes-configuration)

---

## 🌍 ENVIRONMENT CONFIGURATION

### Standard .env.example Template

```bash
# ==============================================================================
# GRAVITY MICROSERVICES - SERVICE CONFIGURATION
# ==============================================================================
# Service: ##-service-name
# Version: 1.0.0
# Last Updated: 2025-11-10
# ==============================================================================

# ------------------------------------------------------------------------------
# APPLICATION SETTINGS
# ------------------------------------------------------------------------------
SERVICE_NAME=service-name
SERVICE_VERSION=1.0.0
ENVIRONMENT=development  # development | staging | production
DEBUG=true
PORT=8001
HOST=0.0.0.0
LOG_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR | CRITICAL

# ------------------------------------------------------------------------------
# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# PostgreSQL Primary Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/service_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
DB_ECHO=false  # Set to true for SQL query logging

# Database Schema (for multi-schema databases)
DB_SCHEMA=service_schema

# ------------------------------------------------------------------------------
# REDIS CONFIGURATION
# ------------------------------------------------------------------------------
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_POOL_SIZE=10
REDIS_MAX_CONNECTIONS=50
REDIS_DECODE_RESPONSES=true

# Cache TTL (seconds)
CACHE_TTL_SHORT=300      # 5 minutes
CACHE_TTL_MEDIUM=1800    # 30 minutes
CACHE_TTL_LONG=3600      # 1 hour

# ------------------------------------------------------------------------------
# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# JWT Settings
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
ALLOWED_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
ALLOWED_HEADERS=*
ALLOW_CREDENTIALS=true

# API Key for service-to-service communication
API_KEY=your-service-api-key-change-this

# ------------------------------------------------------------------------------
# SERVICE DISCOVERY
# ------------------------------------------------------------------------------
# Consul Configuration
CONSUL_HOST=localhost
CONSUL_PORT=8500
CONSUL_SCHEME=http
SERVICE_DISCOVERY_ENABLED=true

# Service Registration
SERVICE_DISCOVERY_URL=http://localhost:8761
SERVICE_HOST=localhost
SERVICE_PORT=8001

# ------------------------------------------------------------------------------
# EXTERNAL SERVICE URLs
# ------------------------------------------------------------------------------
# Core Services
AUTH_SERVICE_URL=http://localhost:8001
USER_SERVICE_URL=http://localhost:8002
NOTIFICATION_SERVICE_URL=http://localhost:8003
FILE_STORAGE_SERVICE_URL=http://localhost:8004

# API Gateway
API_GATEWAY_URL=http://localhost:8000

# ------------------------------------------------------------------------------
# MESSAGE BROKER CONFIGURATION
# ------------------------------------------------------------------------------
# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_EXCHANGE=gravity.events
RABBITMQ_QUEUE_PREFIX=gravity

# Kafka (if used)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_CONSUMER_GROUP=service-name-group
KAFKA_AUTO_OFFSET_RESET=earliest

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION (if service sends emails)
# ------------------------------------------------------------------------------
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@gravity.com
SMTP_FROM_NAME=Gravity Platform
SMTP_USE_TLS=true

# SendGrid (alternative)
SENDGRID_API_KEY=your-sendgrid-api-key

# ------------------------------------------------------------------------------
# SMS CONFIGURATION (if service sends SMS)
# ------------------------------------------------------------------------------
SMS_PROVIDER=twilio  # twilio | kavenegar | ghasedak
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Iranian SMS providers
KAVENEGAR_API_KEY=your-kavenegar-api-key
GHASEDAK_API_KEY=your-ghasedak-api-key

# ------------------------------------------------------------------------------
# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Local Storage
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=gravity-uploads
S3_ENDPOINT_URL=  # For MinIO or custom S3-compatible storage

# MinIO (S3-compatible)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false

# ------------------------------------------------------------------------------
# PAYMENT GATEWAYS (if payment service)
# ------------------------------------------------------------------------------
# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox  # sandbox | live

# ------------------------------------------------------------------------------
# MONITORING & OBSERVABILITY
# ------------------------------------------------------------------------------
# Prometheus
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090

# Jaeger Tracing
JAEGER_ENABLED=true
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831
JAEGER_SAMPLER_TYPE=const
JAEGER_SAMPLER_PARAM=1

# Sentry Error Tracking
SENTRY_DSN=
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.1

# ------------------------------------------------------------------------------
# RATE LIMITING
# ------------------------------------------------------------------------------
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# ------------------------------------------------------------------------------
# FEATURE FLAGS
# ------------------------------------------------------------------------------
FEATURE_CACHE_ENABLED=true
FEATURE_EVENTS_ENABLED=true
FEATURE_NOTIFICATIONS_ENABLED=true
FEATURE_ANALYTICS_ENABLED=false

# ------------------------------------------------------------------------------
# TESTING
# ------------------------------------------------------------------------------
# Test Database (separate from production)
TEST_DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/test_db
```

---

## ⚙️ APPLICATION CONFIGURATION

### Standard config.py Template

```python
"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : config.py
Description  : Application configuration management with Pydantic settings
Language     : Python 3.11+
================================================================================
"""

from typing import List, Optional
from functools import lru_cache
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses Pydantic Settings for validation and type safety.
    All values can be overridden via environment variables.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # -------------------------------------------------------------------------
    # APPLICATION SETTINGS
    # -------------------------------------------------------------------------
    service_name: str = Field(default="service-name")
    service_version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    port: int = Field(default=8000)
    host: str = Field(default="0.0.0.0")
    log_level: str = Field(default="INFO")
    
    # -------------------------------------------------------------------------
    # DATABASE CONFIGURATION
    # -------------------------------------------------------------------------
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/db"
    )
    db_pool_size: int = Field(default=20)
    db_max_overflow: int = Field(default=10)
    db_pool_timeout: int = Field(default=30)
    db_pool_recycle: int = Field(default=3600)
    db_echo: bool = Field(default=False)
    db_schema: Optional[str] = Field(default=None)
    
    # -------------------------------------------------------------------------
    # REDIS CONFIGURATION
    # -------------------------------------------------------------------------
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_password: Optional[str] = Field(default=None)
    redis_pool_size: int = Field(default=10)
    redis_max_connections: int = Field(default=50)
    redis_decode_responses: bool = Field(default=True)
    
    # Cache TTL
    cache_ttl_short: int = Field(default=300)      # 5 minutes
    cache_ttl_medium: int = Field(default=1800)    # 30 minutes
    cache_ttl_long: int = Field(default=3600)      # 1 hour
    
    # -------------------------------------------------------------------------
    # SECURITY CONFIGURATION
    # -------------------------------------------------------------------------
    jwt_secret_key: str = Field(default="change-this-secret-key")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)
    jwt_refresh_token_expire_days: int = Field(default=30)
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    allowed_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    )
    allowed_headers: List[str] = Field(default=["*"])
    allow_credentials: bool = Field(default=True)
    
    # API Key
    api_key: Optional[str] = Field(default=None)
    
    # -------------------------------------------------------------------------
    # SERVICE DISCOVERY
    # -------------------------------------------------------------------------
    consul_host: str = Field(default="localhost")
    consul_port: int = Field(default=8500)
    consul_scheme: str = Field(default="http")
    service_discovery_enabled: bool = Field(default=True)
    service_discovery_url: str = Field(default="http://localhost:8761")
    service_host: str = Field(default="localhost")
    service_port: int = Field(default=8000)
    
    # -------------------------------------------------------------------------
    # EXTERNAL SERVICE URLS
    # -------------------------------------------------------------------------
    auth_service_url: str = Field(default="http://localhost:8001")
    user_service_url: str = Field(default="http://localhost:8002")
    notification_service_url: str = Field(default="http://localhost:8003")
    file_storage_service_url: str = Field(default="http://localhost:8004")
    api_gateway_url: str = Field(default="http://localhost:8000")
    
    # -------------------------------------------------------------------------
    # MESSAGE BROKER
    # -------------------------------------------------------------------------
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/")
    rabbitmq_exchange: str = Field(default="gravity.events")
    rabbitmq_queue_prefix: str = Field(default="gravity")
    
    kafka_bootstrap_servers: str = Field(default="localhost:9092")
    kafka_consumer_group: str = Field(default="service-group")
    kafka_auto_offset_reset: str = Field(default="earliest")
    
    # -------------------------------------------------------------------------
    # EMAIL CONFIGURATION
    # -------------------------------------------------------------------------
    smtp_host: Optional[str] = Field(default=None)
    smtp_port: int = Field(default=587)
    smtp_username: Optional[str] = Field(default=None)
    smtp_password: Optional[str] = Field(default=None)
    smtp_from_email: Optional[str] = Field(default=None)
    smtp_from_name: str = Field(default="Gravity Platform")
    smtp_use_tls: bool = Field(default=True)
    sendgrid_api_key: Optional[str] = Field(default=None)
    
    # -------------------------------------------------------------------------
    # STORAGE CONFIGURATION
    # -------------------------------------------------------------------------
    upload_dir: str = Field(default="./uploads")
    max_upload_size: int = Field(default=10485760)  # 10MB
    
    # AWS S3
    aws_access_key_id: Optional[str] = Field(default=None)
    aws_secret_access_key: Optional[str] = Field(default=None)
    aws_region: str = Field(default="us-east-1")
    s3_bucket_name: Optional[str] = Field(default=None)
    s3_endpoint_url: Optional[str] = Field(default=None)
    
    # -------------------------------------------------------------------------
    # MONITORING
    # -------------------------------------------------------------------------
    prometheus_enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=9090)
    
    jaeger_enabled: bool = Field(default=False)
    jaeger_agent_host: str = Field(default="localhost")
    jaeger_agent_port: int = Field(default=6831)
    
    sentry_dsn: Optional[str] = Field(default=None)
    sentry_environment: str = Field(default="development")
    sentry_traces_sample_rate: float = Field(default=0.1)
    
    # -------------------------------------------------------------------------
    # RATE LIMITING
    # -------------------------------------------------------------------------
    rate_limit_enabled: bool = Field(default=True)
    rate_limit_per_minute: int = Field(default=60)
    rate_limit_per_hour: int = Field(default=1000)
    
    # -------------------------------------------------------------------------
    # FEATURE FLAGS
    # -------------------------------------------------------------------------
    feature_cache_enabled: bool = Field(default=True)
    feature_events_enabled: bool = Field(default=True)
    feature_notifications_enabled: bool = Field(default=True)
    feature_analytics_enabled: bool = Field(default=False)
    
    # -------------------------------------------------------------------------
    # VALIDATORS
    # -------------------------------------------------------------------------
    
    @validator("allowed_origins", pre=True)
    def parse_origins(cls, v):
        """Parse comma-separated origins string."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment value."""
        valid_envs = ["development", "staging", "production"]
        if v not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v_upper
    
    # -------------------------------------------------------------------------
    # COMPUTED PROPERTIES
    # -------------------------------------------------------------------------
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"
    
    @property
    def consul_url(self) -> str:
        """Get full Consul URL."""
        return f"{self.consul_scheme}://{self.consul_host}:{self.consul_port}"
    
    @property
    def service_url(self) -> str:
        """Get full service URL for registration."""
        return f"http://{self.service_host}:{self.service_port}"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Global settings instance
settings = get_settings()
```

---

## 🗄️ DATABASE CONFIGURATION

### Standard database.py Template

```python
"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : database.py
Description  : Database connection and session management
Language     : Python 3.11+
================================================================================
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
import structlog

from app.config import settings

logger = structlog.get_logger()

# -------------------------------------------------------------------------
# DATABASE ENGINE
# -------------------------------------------------------------------------

def create_database_engine() -> AsyncEngine:
    """
    Create async database engine with connection pooling.
    
    Returns:
        AsyncEngine: Configured database engine
    """
    pool_class = NullPool if settings.is_development else QueuePool
    
    engine = create_async_engine(
        settings.database_url,
        echo=settings.db_echo,
        poolclass=pool_class,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_timeout=settings.db_pool_timeout,
        pool_recycle=settings.db_pool_recycle,
        pool_pre_ping=True,  # Verify connections before using
    )
    
    logger.info(
        "database_engine_created",
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow
    )
    
    return engine


# Global engine instance
engine = create_database_engine()

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


# -------------------------------------------------------------------------
# DATABASE SESSION DEPENDENCY
# -------------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error("database_session_error", error=str(e), exc_info=True)
            raise
        finally:
            await session.close()


# -------------------------------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------------------------------

async def init_database():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("database_initialized")


async def close_database():
    """Close database connections."""
    await engine.dispose()
    logger.info("database_connections_closed")
```

---

## 🔴 REDIS CONFIGURATION

### Standard redis_client.py Template

```python
"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : redis_client.py
Description  : Redis client configuration and helpers
Language     : Python 3.11+
================================================================================
"""

from typing import Optional, Any
import json
from redis import asyncio as aioredis
import structlog

from app.config import settings

logger = structlog.get_logger()


class RedisClient:
    """Async Redis client with helper methods."""
    
    def __init__(self):
        """Initialize Redis client."""
        self.redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        self.redis = await aioredis.from_url(
            settings.redis_url,
            password=settings.redis_password,
            encoding="utf-8",
            decode_responses=settings.redis_decode_responses,
            max_connections=settings.redis_max_connections
        )
        
        # Test connection
        await self.redis.ping()
        logger.info("redis_connected", url=settings.redis_url)
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("redis_disconnected")
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        return await self.redis.get(key)
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set key-value pair with optional TTL."""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        if ttl:
            return await self.redis.setex(key, ttl, value)
        return await self.redis.set(key, value)
    
    async def delete(self, key: str) -> int:
        """Delete key."""
        return await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.redis.exists(key)
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment key value."""
        return await self.redis.incrby(key, amount)
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL on key."""
        return await self.redis.expire(key, ttl)
    
    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value by key."""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set_json(
        self,
        key: str,
        value: dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Set JSON value."""
        return await self.set(key, json.dumps(value), ttl)


# Global Redis client
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """Dependency to get Redis client."""
    return redis_client
```

---

## 🔐 SECURITY CONFIGURATION

### Standard security.py Template

```python
"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : security.py
Description  : Security utilities (JWT, password hashing, etc.)
Language     : Python 3.11+
================================================================================
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import structlog

from app.config import settings

logger = structlog.get_logger()

# -------------------------------------------------------------------------
# PASSWORD HASHING
# -------------------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------------------------------------------------
# JWT TOKEN MANAGEMENT
# -------------------------------------------------------------------------

security = HTTPBearer()


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Payload data to encode
        expires_delta: Token expiration time
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        dict: Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        logger.warning("jwt_decode_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Get current user from JWT token.
    
    Dependency for protected endpoints.
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            ...
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    return payload


async def verify_api_key(api_key: str) -> bool:
    """Verify API key for service-to-service communication."""
    if not settings.api_key:
        return True  # API key not configured
    
    return api_key == settings.api_key
```

---

## 📝 LOGGING CONFIGURATION

### Standard logging_config.py Template

```python
"""
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity MicroServices Platform
File         : logging_config.py
Description  : Structured logging configuration
Language     : Python 3.11+
================================================================================
"""

import logging
import structlog
from typing import Any

from app.config import settings


def setup_logging():
    """Configure structured logging with structlog."""
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.log_level),
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.dev.ConsoleRenderer() if settings.is_development
            else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


# Setup logging on module import
setup_logging()
```

---

## 🐳 DOCKER CONFIGURATION

### Standard Dockerfile Template

```dockerfile
# ==============================================================================
# GRAVITY MICROSERVICES - SERVICE DOCKERFILE
# ==============================================================================
# Service: ##-service-name
# Base Image: Python 3.11 Alpine
# Multi-stage build for minimal image size
# ==============================================================================

# ------------------------------------------------------------------------------
# STAGE 1: Builder
# ------------------------------------------------------------------------------
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.0

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# ------------------------------------------------------------------------------
# STAGE 2: Runtime
# ------------------------------------------------------------------------------
FROM python:3.11-alpine

# Install runtime dependencies
RUN apk add --no-cache \
    postgresql-libs \
    libffi \
    openssl

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser ./app ./app
COPY --chown=appuser:appuser ./alembic ./alembic
COPY --chown=appuser:appuser ./alembic.ini ./

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Standard docker-compose.yml Template

```yaml
# ==============================================================================
# GRAVITY MICROSERVICES - DOCKER COMPOSE
# ==============================================================================
# Service: ##-service-name
# Environment: Development
# ==============================================================================

version: '3.8'

services:
  # ----------------------------------------------------------------------------
  # APPLICATION SERVICE
  # ----------------------------------------------------------------------------
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: service-name
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/service_db
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./app:/app/app:ro
      - ./tests:/app/tests:ro
    networks:
      - gravity-network
    restart: unless-stopped
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # ----------------------------------------------------------------------------
  # POSTGRESQL DATABASE
  # ----------------------------------------------------------------------------
  postgres:
    image: postgres:16-alpine
    container_name: service-postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=service_db
      - PGDATA=/var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - gravity-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ----------------------------------------------------------------------------
  # REDIS CACHE
  # ----------------------------------------------------------------------------
  redis:
    image: redis:7-alpine
    container_name: service-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - gravity-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    command: redis-server --appendonly yes

# ------------------------------------------------------------------------------
# VOLUMES
# ------------------------------------------------------------------------------
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

# ------------------------------------------------------------------------------
# NETWORKS
# ------------------------------------------------------------------------------
networks:
  gravity-network:
    driver: bridge
```

---

## ☸️ KUBERNETES CONFIGURATION

### Standard deployment.yaml Template

```yaml
# ==============================================================================
# KUBERNETES DEPLOYMENT - SERVICE
# ==============================================================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-name
  namespace: gravity
  labels:
    app: service-name
    version: v1
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: service-name
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: service-name
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: service-name-sa
      
      # Init containers
      initContainers:
      - name: wait-for-postgres
        image: busybox:1.35
        command:
          - 'sh'
          - '-c'
          - 'until nc -z postgres-service 5432; do echo waiting for postgres; sleep 2; done;'
      
      # Application container
      containers:
      - name: service-name
        image: gravity/service-name:latest
        imagePullPolicy: Always
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP
        
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: PORT
          value: "8000"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: service-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: service-secrets
              key: redis-url
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: service-secrets
              key: jwt-secret
        
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      
      volumes:
      - name: config
        configMap:
          name: service-config

---
# ==============================================================================
# KUBERNETES SERVICE
# ==============================================================================
apiVersion: v1
kind: Service
metadata:
  name: service-name
  namespace: gravity
  labels:
    app: service-name
spec:
  type: ClusterIP
  selector:
    app: service-name
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: metrics
    protocol: TCP

---
# ==============================================================================
# HORIZONTAL POD AUTOSCALER
# ==============================================================================
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: service-name-hpa
  namespace: gravity
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: service-name
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max
```

---

## 📚 USAGE GUIDE

### Setting Up a New Service

1. **Copy Configuration Templates**
   ```bash
   # Copy .env.example to .env
   cp .env.example .env
   
   # Edit environment variables
   nano .env
   ```

2. **Install Dependencies**
   ```bash
   poetry install
   ```

3. **Run Database Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start Development Server**
   ```bash
   # With Docker Compose
   docker-compose up -d
   
   # Or directly
   uvicorn app.main:app --reload
   ```

5. **Run Tests**
   ```bash
   pytest tests/ -v --cov=app
   ```

### Production Deployment

1. **Build Docker Image**
   ```bash
   docker build -t gravity/service-name:1.0.0 .
   ```

2. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Verify Deployment**
   ```bash
   kubectl get pods -n gravity
   kubectl logs -f deployment/service-name -n gravity
   ```

---

**Questions? See:**
- `COMPLETE_ARCHITECTURE.md` - Full architecture guide
- `TEAM_PROMPT.md` - Team standards
- Individual service README files

---

*Last Updated: November 10, 2025*  
*Maintained by: Gravity Elite Engineering Team*
