#!/usr/bin/env pwsh
# ================================================================================
# Standardize config.py for Priority 1 Services (10 services)
# ================================================================================
# This script ensures all Priority 1 services have proper Pydantic Settings
# configuration following TEAM_PROMPT.md standards
# ================================================================================

param(
    [switch]$DryRun = $false,
    [string[]]$Services = @(
        "01-common-library",
        "02-service-discovery", 
        "03-api-gateway",
        "04-config-service",
        "05-auth-service",
        "06-user-service",
        "07-notification-service",
        "08-email-service",
        "09-sms-service",
        "10-file-storage-service"
    )
)

$ErrorActionPreference = "Stop"

function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }

Write-Info "⚙️  Standardizing config.py for Priority 1 Services"
Write-Info "====================================================="

# Get port mapping
function Get-ServicePorts {
    param([string]$ServiceName)
    
    if ($ServiceName -match '^(\d{2})-') {
        $num = [int]$matches[1]
        return @{
            DB    = 5400 + $num
            Redis = 6300 + $num
            App   = 8000 + $num
        }
    }
    return $null
}

# Standard config.py template
$configTemplate = @'
"""
================================================================================
FILE IDENTITY (شناسنامه فایل)
================================================================================
Project      : Gravity MicroServices Platform
File         : config.py
Description  : Configuration settings for {SERVICE_NAME_DISPLAY}
Language     : English (UK)
Framework    : FastAPI / Python 3.12+

================================================================================
AUTHORSHIP & CONTRIBUTION (مشارکت‌کنندگان)
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : Elite Engineering Team
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT (زمان‌بندی و تلاش)
================================================================================
Created Date      : 2025-11-12 00:00 UTC
Last Modified     : 2025-11-12 00:00 UTC
Development Time  : 0 hours 30 minutes
Total Cost        : 0.5 × $150 = $75.00 USD

================================================================================
VERSION HISTORY (تاریخچه نسخه)
================================================================================
v1.0.0 - 2025-11-12 - Dr. Sarah Chen - Standardized configuration
v1.0.1 - 2025-11-12 - Auto-generated with proper type hints and validation

================================================================================
DEPENDENCIES (وابستگی‌ها)
================================================================================
Internal  : None
External  : pydantic-settings>=2.0.0, pydantic>=2.0.0
Database  : PostgreSQL 16+, Redis 7

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/{SERVICE_NAME}

================================================================================
"""

from typing import Optional, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables or .env file.
    Follows 12-factor app configuration principles.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # ==============================================================================
    # Application Configuration
    # ==============================================================================
    APP_NAME: str = Field(default="{SERVICE_NAME}", description="Service name")
    APP_VERSION: str = Field(default="1.0.0", description="Service version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    PORT: int = Field(default={APP_PORT}, description="Application port")
    
    # ==============================================================================
    # Database Configuration (PostgreSQL)
    # ==============================================================================
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:{DB_PORT}/{DB_NAME}",
        description="PostgreSQL connection URL"
    )
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default={DB_PORT}, description="Database port")
    DB_NAME: str = Field(default="{DB_NAME}", description="Database name")
    DB_USER: str = Field(default="postgres", description="Database user")
    DB_PASSWORD: str = Field(default="postgres", description="Database password")
    DB_POOL_SIZE: int = Field(default=10, description="Connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=20, description="Max pool overflow")
    DB_POOL_TIMEOUT: int = Field(default=30, description="Pool timeout in seconds")
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # ==============================================================================
    # Redis Configuration
    # ==============================================================================
    REDIS_URL: str = Field(
        default="redis://localhost:{REDIS_PORT}/0",
        description="Redis connection URL"
    )
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default={REDIS_PORT}, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_MAX_CONNECTIONS: int = Field(default=50, description="Max Redis connections")
    
    # ==============================================================================
    # Security Configuration
    # ==============================================================================
    SECRET_KEY: str = Field(
        default="change-in-production-min-32-chars-12345",
        min_length=32,
        description="Application secret key"
    )
    JWT_SECRET_KEY: str = Field(
        default="change-jwt-secret-in-production-12345",
        min_length=32,
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration in days"
    )
    
    # ==============================================================================
    # CORS Configuration
    # ==============================================================================
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        description="Comma-separated list of allowed origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="Allow credentials in CORS"
    )
    CORS_ALLOW_METHODS: str = Field(
        default="GET,POST,PUT,DELETE,PATCH,OPTIONS",
        description="Allowed HTTP methods"
    )
    CORS_ALLOW_HEADERS: str = Field(default="*", description="Allowed headers")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # ==============================================================================
    # Rate Limiting
    # ==============================================================================
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Requests per minute")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, description="Requests per hour")
    
    # ==============================================================================
    # Service Discovery (Consul)
    # ==============================================================================
    CONSUL_HOST: str = Field(default="localhost", description="Consul host")
    CONSUL_PORT: int = Field(default=8500, description="Consul port")
    SERVICE_DISCOVERY_ENABLED: bool = Field(
        default=False,
        description="Enable service discovery"
    )
    
    # ==============================================================================
    # External Services URLs
    # ==============================================================================
    API_GATEWAY_URL: str = Field(
        default="http://localhost:8003",
        description="API Gateway URL"
    )
    AUTH_SERVICE_URL: str = Field(
        default="http://localhost:8005",
        description="Auth Service URL"
    )
    USER_SERVICE_URL: str = Field(
        default="http://localhost:8006",
        description="User Service URL"
    )
    NOTIFICATION_SERVICE_URL: str = Field(
        default="http://localhost:8007",
        description="Notification Service URL"
    )
    
    # ==============================================================================
    # Monitoring & Observability
    # ==============================================================================
    METRICS_ENABLED: bool = Field(default=True, description="Enable Prometheus metrics")
    METRICS_PORT: int = Field(default=9090, description="Metrics port")
    TRACING_ENABLED: bool = Field(default=False, description="Enable Jaeger tracing")
    JAEGER_HOST: str = Field(default="localhost", description="Jaeger host")
    JAEGER_PORT: int = Field(default=6831, description="Jaeger port")
    
    # ==============================================================================
    # Testing Configuration
    # ==============================================================================
    TEST_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/test_{DB_NAME}",
        description="Test database URL"
    )
    TEST_REDIS_URL: str = Field(
        default="redis://localhost:6379/15",
        description="Test Redis URL"
    )
    
    # ==============================================================================
    # API Documentation
    # ==============================================================================
    API_TITLE: str = Field(
        default="{SERVICE_NAME_DISPLAY} API",
        description="API title"
    )
    API_DESCRIPTION: str = Field(
        default="Independent {SERVICE_NAME_DISPLAY} Microservice",
        description="API description"
    )
    API_VERSION: str = Field(default="1.0.0", description="API version")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the accepted values."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()
    
    @field_validator("SECRET_KEY", "JWT_SECRET_KEY")
    @classmethod
    def validate_secret_keys(cls, v: str) -> str:
        """Ensure secret keys are not default values in production."""
        if "change" in v.lower() or "secret" in v.lower():
            import os
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise ValueError("Must set secure SECRET_KEY in production")
        return v


# ==============================================================================
# Service-Specific Configuration
# ==============================================================================
{SERVICE_SPECIFIC_CONFIG}


# ==============================================================================
# Global Settings Instance
# ==============================================================================
settings = Settings()


# ==============================================================================
# Configuration Validation on Import
# ==============================================================================
if __name__ == "__main__":
    # Print configuration (excluding sensitive data)
    print(f"✅ Configuration loaded for: {settings.APP_NAME}")
    print(f"   Version: {settings.APP_VERSION}")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Port: {settings.PORT}")
    print(f"   Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"   Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    print(f"   Debug Mode: {settings.DEBUG}")
    print(f"   Log Level: {settings.LOG_LEVEL}")
'@

# Service-specific configurations
$serviceSpecificConfigs = @{
    "01-common-library"       = ""  # No specific config for library
    "02-service-discovery"    = @"
class ServiceDiscoverySettings(Settings):
    """Extended settings for Service Discovery."""
    
    # Consul specific
    CONSUL_DATACENTER: str = Field(default="dc1", description="Consul datacenter")
    CONSUL_TOKEN: Optional[str] = Field(default=None, description="Consul ACL token")
    
    # Service registration
    SERVICE_TTL: int = Field(default=30, description="Service TTL in seconds")
    HEALTH_CHECK_INTERVAL: str = Field(default="10s", description="Health check interval")
    HEALTH_CHECK_TIMEOUT: str = Field(default="5s", description="Health check timeout")
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = Field(default=30, description="WebSocket heartbeat interval")
    WS_MAX_CONNECTIONS: int = Field(default=1000, description="Max WebSocket connections")


settings = ServiceDiscoverySettings()
"@
    "03-api-gateway"          = @"
class ApiGatewaySettings(Settings):
    """Extended settings for API Gateway."""
    
    # Rate limiting
    GLOBAL_RATE_LIMIT: int = Field(default=10000, description="Global rate limit per hour")
    
    # Circuit breaker
    CIRCUIT_BREAKER_ENABLED: bool = Field(default=True, description="Enable circuit breaker")
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = Field(default=5, description="Failure threshold")
    CIRCUIT_BREAKER_TIMEOUT: int = Field(default=60, description="Circuit breaker timeout")
    
    # Load balancing
    LOAD_BALANCE_STRATEGY: str = Field(default="round_robin", description="Load balance strategy")


settings = ApiGatewaySettings()
"@
    "04-config-service"       = ""
    "05-auth-service"         = @"
class AuthServiceSettings(Settings):
    """Extended settings for Auth Service."""
    
    # OAuth2 providers
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google OAuth secret")
    GITHUB_CLIENT_ID: Optional[str] = Field(default=None, description="GitHub OAuth client ID")
    GITHUB_CLIENT_SECRET: Optional[str] = Field(default=None, description="GitHub OAuth secret")
    
    # Password policy
    PASSWORD_MIN_LENGTH: int = Field(default=8, description="Minimum password length")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(default=True, description="Require uppercase")
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(default=True, description="Require lowercase")
    PASSWORD_REQUIRE_DIGIT: bool = Field(default=True, description="Require digit")
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True, description="Require special character")
    
    # Session
    SESSION_COOKIE_NAME: str = Field(default="session_id", description="Session cookie name")
    SESSION_EXPIRE_SECONDS: int = Field(default=3600, description="Session expiration")


settings = AuthServiceSettings()
"@
    "06-user-service"         = ""
    "07-notification-service" = @"
class NotificationServiceSettings(Settings):
    """Extended settings for Notification Service."""
    
    # Email provider
    EMAIL_PROVIDER: str = Field(default="smtp", description="Email provider (smtp/sendgrid)")
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USER: Optional[str] = Field(default=None, description="SMTP user")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    
    # SMS provider
    SMS_PROVIDER: str = Field(default="twilio", description="SMS provider")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, description="Twilio SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, description="Twilio token")
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None, description="Twilio phone")
    
    # Push notifications
    FCM_SERVER_KEY: Optional[str] = Field(default=None, description="FCM server key")


settings = NotificationServiceSettings()
"@
    "08-email-service"        = @"
class EmailServiceSettings(Settings):
    """Extended settings for Email Service."""
    
    # SMTP Configuration
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USER: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    SMTP_FROM_NAME: str = Field(default="GravityWaves", description="From name")
    SMTP_FROM_EMAIL: str = Field(default="noreply@gravitywaves.com", description="From email")
    
    # SendGrid alternative
    SENDGRID_API_KEY: Optional[str] = Field(default=None, description="SendGrid API key")
    
    # Templates
    TEMPLATE_DIR: str = Field(default="app/templates/email", description="Template directory")


settings = EmailServiceSettings()
"@
    "09-sms-service"          = @"
class SmsServiceSettings(Settings):
    """Extended settings for SMS Service."""
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, description="Twilio Account SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, description="Twilio Auth Token")
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None, description="Twilio Phone Number")
    
    # AWS SNS Alternative
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS Access Key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS Secret Key")
    AWS_REGION: str = Field(default="us-east-1", description="AWS Region")


settings = SmsServiceSettings()
"@
    "10-file-storage-service" = @"
class FileStorageServiceSettings(Settings):
    """Extended settings for File Storage Service."""
    
    # Storage backend
    STORAGE_BACKEND: str = Field(default="local", description="Storage backend (local/s3)")
    STORAGE_PATH: str = Field(default="./uploads", description="Local storage path")
    
    # S3 Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS Access Key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS Secret Key")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, description="S3 Bucket name")
    AWS_REGION: str = Field(default="us-east-1", description="AWS Region")
    
    # File upload limits
    MAX_FILE_SIZE_MB: int = Field(default=10, description="Max file size in MB")
    ALLOWED_EXTENSIONS: str = Field(
        default="jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx",
        description="Allowed file extensions"
    )
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions from comma-separated string."""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]


settings = FileStorageServiceSettings()
"@
}

$created = 0
$updated = 0
$skipped = 0

foreach ($serviceName in $Services) {
    $servicePath = Join-Path $PWD $serviceName
    
    if (-not (Test-Path $servicePath)) {
        Write-Warn "⚠️  Service not found: $serviceName"
        continue
    }
    
    $configPath = Join-Path $servicePath "app\config.py"
    $ports = Get-ServicePorts $serviceName
    
    if (-not $ports) {
        Write-Warn "⚠️  Could not determine ports for $serviceName"
        continue
    }
    
    Write-Info "`n📦 Processing: $serviceName"
    
    # Generate service display name
    $serviceDisplay = $serviceName -replace '^\d{2}-', '' -replace '-', ' '
    $serviceDisplay = (Get-Culture).TextInfo.ToTitleCase($serviceDisplay)
    
    # Generate database name
    $dbName = $serviceName -replace '^\d{2}-', '' -replace '-', '_'
    
    # Get service-specific config
    $serviceSpecific = $serviceSpecificConfigs[$serviceName]
    if (-not $serviceSpecific) {
        $serviceSpecific = ""
    }
    
    # Generate config content
    $configContent = $configTemplate `
        -replace '{SERVICE_NAME}', $serviceName `
        -replace '{SERVICE_NAME_DISPLAY}', $serviceDisplay `
        -replace '{APP_PORT}', $ports.App `
        -replace '{DB_PORT}', $ports.DB `
        -replace '{REDIS_PORT}', $ports.Redis `
        -replace '{DB_NAME}', $dbName `
        -replace '{SERVICE_SPECIFIC_CONFIG}', $serviceSpecific
    
    # Check if config.py exists
    if (Test-Path $configPath) {
        # Read existing config
        $existingContent = Get-Content $configPath -Raw
        
        # Check if it's already a good config (has BaseSettings and proper structure)
        if ($existingContent -match 'class Settings\(BaseSettings\):' -and 
            $existingContent -match 'model_config' -and 
            $existingContent -match 'DATABASE_URL.*Field' -and
            $existingContent.Length -gt 3000) {
            Write-Success "  ✅ Config already comprehensive - skipped"
            $skipped++
            continue
        }
        
        Write-Warn "  ⚠️  Existing config.py found (not comprehensive)"
        
        if (-not $DryRun) {
            # Backup existing file
            $backupPath = "$configPath.backup"
            Copy-Item $configPath $backupPath
            Write-Info "  💾 Backup created: config.py.backup"
            
            # Write new file
            Set-Content -Path $configPath -Value $configContent -NoNewline
            Write-Success "  ✅ config.py updated with comprehensive settings"
            $updated++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would update config.py"
        }
    }
    else {
        Write-Warn "  ⚠️  config.py not found"
        
        if (-not $DryRun) {
            # Ensure app directory exists
            $appDir = Join-Path $servicePath "app"
            if (-not (Test-Path $appDir)) {
                New-Item -ItemType Directory -Path $appDir -Force | Out-Null
            }
            
            Set-Content -Path $configPath -Value $configContent -NoNewline
            Write-Success "  ✅ config.py created"
            $created++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would create config.py"
        }
    }
}

Write-Info "`n====================================================="
Write-Info "📊 Summary:"
Write-Success "  ✅ Created: $created"
Write-Success "  📝 Updated: $updated"
Write-Info "  ⏭️  Skipped: $skipped (already comprehensive)"
Write-Info "  📦 Total: $($Services.Count)"
Write-Info "====================================================="

if ($DryRun) {
    Write-Warn "`n⚠️  DRY RUN MODE - No files were modified"
    Write-Info "Run without -DryRun to apply changes"
}

Write-Info "`n💡 Next Steps:"
Write-Info "  1. Review generated config.py files"
Write-Info "  2. Validate settings with: python -m app.config"
Write-Info "  3. Update .env files to match new settings"
Write-Info "  4. Run MyPy for type checking"
