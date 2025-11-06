"""
Configuration settings for API Gateway.

Enterprise-grade configuration management following 12-factor app principles.
All settings loaded from environment variables for deployment flexibility.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    API Gateway configuration settings.
    
    All values can be overridden via environment variables.
    Designed by Elite Team with 180+ IQ for production excellence.
    """
    
    # Application
    APP_NAME: str = "api-gateway"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_VERSION: str = "1.0.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    WORKERS: int = 4
    
    # Redis for rate limiting and caching
    REDIS_URL: str = "redis://localhost:6379/1"
    REDIS_MAX_CONNECTIONS: int = 50
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "change-this-jwt-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    CORS_CREDENTIALS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 100
    RATE_LIMIT_REQUESTS_PER_HOUR: int = 5000
    
    # Circuit Breaker
    CIRCUIT_BREAKER_ENABLED: bool = True
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    CIRCUIT_BREAKER_SUCCESS_THRESHOLD: int = 2
    CIRCUIT_BREAKER_TIMEOUT: int = 60
    
    # Proxy Configuration
    PROXY_CONNECT_TIMEOUT: float = 5.0
    PROXY_READ_TIMEOUT: float = 30.0
    PROXY_WRITE_TIMEOUT: float = 30.0
    PROXY_POOL_TIMEOUT: float = 5.0
    
    # Service URLs (Backend microservices)
    AUTH_SERVICE_URL: str = "http://localhost:8081"
    USER_SERVICE_URL: str = "http://localhost:8082"
    NOTIFICATION_SERVICE_URL: str = "http://localhost:8083"
    FILE_SERVICE_URL: str = "http://localhost:8084"
    PAYMENT_SERVICE_URL: str = "http://localhost:8085"
    ANALYTICS_SERVICE_URL: str = "http://localhost:8086"
    
    # Timeouts (in seconds)
    REQUEST_TIMEOUT: int = 30
    CONNECT_TIMEOUT: int = 5
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    
    # Health Check
    HEALTH_CHECK_INTERVAL: int = 30  # seconds
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
