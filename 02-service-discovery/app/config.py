"""
Service Discovery configuration settings.
"""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Service Discovery configuration settings."""
    
    # Application Settings
    APP_NAME: str = "Service Discovery"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, validation_alias="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    
    # API Settings
    API_TITLE: str = "Service Discovery API"
    API_DESCRIPTION: str = "Central service registry and discovery for Gravity MicroServices Platform"
    API_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", validation_alias="HOST")
    PORT: int = Field(default=8761, validation_alias="PORT")
    WORKERS: int = Field(default=4, validation_alias="WORKERS")
    
    # Consul Settings
    CONSUL_HOST: str = Field(default="localhost", validation_alias="CONSUL_HOST")
    CONSUL_PORT: int = Field(default=8500, validation_alias="CONSUL_PORT")
    CONSUL_SCHEME: str = Field(default="http", validation_alias="CONSUL_SCHEME")
    CONSUL_TOKEN: Optional[str] = Field(default=None, validation_alias="CONSUL_TOKEN")
    CONSUL_DATACENTER: str = Field(default="dc1", validation_alias="CONSUL_DATACENTER")
    
    # Service Registration Settings
    SERVICE_TTL: int = Field(default=30, validation_alias="SERVICE_TTL")  # seconds
    SERVICE_DEREGISTER_CRITICAL_AFTER: str = Field(
        default="1m", validation_alias="SERVICE_DEREGISTER_CRITICAL_AFTER"
    )
    HEALTH_CHECK_INTERVAL: str = Field(default="10s", validation_alias="HEALTH_CHECK_INTERVAL")
    HEALTH_CHECK_TIMEOUT: str = Field(default="5s", validation_alias="HEALTH_CHECK_TIMEOUT")
    
    # Database Settings (PostgreSQL)
    POSTGRES_USER: str = Field(default="service_discovery", validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="service_discovery_pass", validation_alias="POSTGRES_PASSWORD")
    POSTGRES_HOST: str = Field(default="localhost", validation_alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    POSTGRES_DB: str = Field(default="service_discovery_db", validation_alias="POSTGRES_DB")
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Redis Settings
    REDIS_HOST: str = Field(default="localhost", validation_alias="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, validation_alias="REDIS_PORT")
    REDIS_DB: int = Field(default=0, validation_alias="REDIS_DB")
    REDIS_PASSWORD: Optional[str] = Field(default=None, validation_alias="REDIS_PASSWORD")
    REDIS_MAX_CONNECTIONS: int = Field(default=10, validation_alias="REDIS_MAX_CONNECTIONS")
    
    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # CORS Settings
    CORS_ORIGINS: str = Field(default="*", validation_alias="CORS_ORIGINS")
    CORS_CREDENTIALS: bool = Field(default=True, validation_alias="CORS_CREDENTIALS")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Load Balancing Settings
    DEFAULT_LB_STRATEGY: str = Field(default="round_robin", validation_alias="DEFAULT_LB_STRATEGY")
    # Options: round_robin, least_connections, weighted, random, geographic
    
    # Cache Settings
    CACHE_TTL: int = Field(default=60, validation_alias="CACHE_TTL")  # seconds
    CACHE_ENABLED: bool = Field(default=True, validation_alias="CACHE_ENABLED")
    
    # WebSocket Settings
    WS_HEARTBEAT_INTERVAL: int = Field(default=30, validation_alias="WS_HEARTBEAT_INTERVAL")  # seconds
    WS_MAX_CONNECTIONS: int = Field(default=1000, validation_alias="WS_MAX_CONNECTIONS")
    
    # Monitoring Settings
    PROMETHEUS_ENABLED: bool = Field(default=True, validation_alias="PROMETHEUS_ENABLED")
    METRICS_PORT: int = Field(default=9090, validation_alias="METRICS_PORT")
    
    # Security Settings
    REQUIRE_AUTHENTICATION: bool = Field(default=False, validation_alias="REQUIRE_AUTHENTICATION")
    API_KEY_HEADER: str = Field(default="X-API-Key", validation_alias="API_KEY_HEADER")
    
    # Multi-Datacenter Settings
    MULTI_DC_ENABLED: bool = Field(default=False, validation_alias="MULTI_DC_ENABLED")
    DATACENTER_NAME: str = Field(default="dc1", validation_alias="DATACENTER_NAME")
    PEER_DATACENTERS: str = Field(default="", validation_alias="PEER_DATACENTERS")
    
    @property
    def peer_datacenters_list(self) -> List[str]:
        """Parse peer datacenters from comma-separated string."""
        if not self.PEER_DATACENTERS:
            return []
        return [dc.strip() for dc in self.PEER_DATACENTERS.split(",")]
    
    # Performance Settings
    MAX_SERVICES_PER_QUERY: int = Field(default=100, validation_alias="MAX_SERVICES_PER_QUERY")
    QUERY_TIMEOUT: int = Field(default=5, validation_alias="QUERY_TIMEOUT")  # seconds
    
    # Feature Flags
    ENABLE_GEOGRAPHIC_ROUTING: bool = Field(default=False, validation_alias="ENABLE_GEOGRAPHIC_ROUTING")
    ENABLE_WEIGHTED_LB: bool = Field(default=True, validation_alias="ENABLE_WEIGHTED_LB")
    ENABLE_CONFIG_MANAGEMENT: bool = Field(default=True, validation_alias="ENABLE_CONFIG_MANAGEMENT")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v_upper
    
    @field_validator("DEFAULT_LB_STRATEGY")
    @classmethod
    def validate_lb_strategy(cls, v: str) -> str:
        """Validate load balancing strategy."""
        valid_strategies = ["round_robin", "least_connections", "weighted", "random", "geographic"]
        if v not in valid_strategies:
            raise ValueError(f"Invalid LB strategy: {v}. Must be one of {valid_strategies}")
        return v


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
