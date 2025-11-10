"""
Application Configuration
"""

from typing import Any, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Service Configuration
    SERVICE_NAME: str = Field(default="template-service", description="Service name")
    SERVICE_VERSION: str = Field(default="1.0.0", description="Service version")
    SERVICE_PORT: int = Field(default=8000, description="Service port")
    ENVIRONMENT: str = Field(default="development", description="Environment (development, staging, production)")

    # API Configuration
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    DEBUG: bool = Field(default=True, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")

    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/template_service",
        description="Database connection URL",
    )
    DATABASE_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, description="Database max overflow connections")
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries")

    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")
    REDIS_MAX_CONNECTIONS: int = Field(default=10, description="Redis max connections")
    REDIS_SOCKET_TIMEOUT: int = Field(default=5, description="Redis socket timeout")

    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT",
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiration")

    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins",
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="CORS allow credentials")
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"], description="CORS allowed methods")
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], description="CORS allowed headers")

    # Service Discovery (Consul)
    CONSUL_HOST: str = Field(default="localhost", description="Consul host")
    CONSUL_PORT: int = Field(default=8500, description="Consul port")
    CONSUL_SCHEME: str = Field(default="http", description="Consul scheme")
    SERVICE_HEALTH_CHECK_INTERVAL: str = Field(default="10s", description="Health check interval")
    SERVICE_HEALTH_CHECK_TIMEOUT: str = Field(default="5s", description="Health check timeout")

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FORMAT: str = Field(default="json", description="Log format (json, text)")
    LOG_FILE_PATH: str = Field(default="logs/service.log", description="Log file path")
    LOG_FILE_MAX_SIZE: int = Field(default=10485760, description="Log file max size (10MB)")
    LOG_FILE_BACKUP_COUNT: int = Field(default=5, description="Log file backup count")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests")
    RATE_LIMIT_PERIOD: int = Field(default=60, description="Rate limit period (seconds)")

    # Circuit Breaker
    CIRCUIT_BREAKER_ENABLED: bool = Field(default=True, description="Enable circuit breaker")
    CIRCUIT_BREAKER_THRESHOLD: int = Field(default=5, description="Circuit breaker failure threshold")
    CIRCUIT_BREAKER_TIMEOUT: int = Field(default=60, description="Circuit breaker timeout")

    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, description="Enable Prometheus metrics")
    METRICS_PORT: int = Field(default=9090, description="Metrics port")
    ENABLE_TRACING: bool = Field(default=True, description="Enable OpenTelemetry tracing")
    JAEGER_HOST: str = Field(default="localhost", description="Jaeger host")
    JAEGER_PORT: int = Field(default=6831, description="Jaeger port")

    # External Services
    AUTH_SERVICE_URL: str = Field(default="http://localhost:8001", description="Auth service URL")
    NOTIFICATION_SERVICE_URL: str = Field(
        default="http://localhost:8002",
        description="Notification service URL",
    )
    API_GATEWAY_URL: str = Field(default="http://localhost:8080", description="API Gateway URL")

    # Cache Configuration
    CACHE_TTL: int = Field(default=300, description="Cache TTL (seconds)")
    CACHE_ENABLED: bool = Field(default=True, description="Enable caching")

    # Worker Configuration
    MAX_WORKERS: int = Field(default=4, description="Max worker threads")
    WORKER_TIMEOUT: int = Field(default=30, description="Worker timeout")

    # Test Configuration
    TEST_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/template_service_test",
        description="Test database URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level"""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment"""
        allowed = ["development", "staging", "production"]
        if v.lower() not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v.lower()

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == "development"


# Create settings instance
settings = Settings()
