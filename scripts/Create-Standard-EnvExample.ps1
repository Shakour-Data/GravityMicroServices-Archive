#!/usr/bin/env pwsh
# ================================================================================
# Create Standard .env.example for Priority 1 Services (10 services)
# ================================================================================
# This script generates standardized .env.example files with all required
# environment variables following TEAM_PROMPT.md standards
# ================================================================================

param(
    [switch]$DryRun = $false,
    [int]$StartFrom = 1,
    [int]$EndAt = 52
)

$ErrorActionPreference = "Stop"

function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }

Write-Info "⚙️  Creating Standard .env.example for Services $StartFrom-$EndAt"
Write-Info "============================================================"

# Get all service directories in range
$allServices = Get-ChildItem -Directory | Where-Object { $_.Name -match '^\d{2}-.*-service$' } | Sort-Object Name
$services = $allServices | Where-Object { 
    if ($_.Name -match '^(\d{2})-') {
        $num = [int]$matches[1]
        $num -ge $StartFrom -and $num -le $EndAt
    }
    else {
        $false
    }
}

# Get port mapping from docker-compose
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

# Standard .env.example template
$envTemplate = @"
# ================================================================================
# Environment Configuration for {SERVICE_NAME}
# ================================================================================
# Following Gravity MicroServices standards from TEAM_PROMPT.md
# 
# ⚠️  SECURITY WARNING:
# - Never commit actual .env file to git
# - Always use strong passwords in production
# - Rotate secrets regularly
# - Use proper secrets management (HashiCorp Vault, AWS Secrets Manager, etc.)
# ================================================================================

# ==============================================================================
# Application Configuration
# ==============================================================================
APP_NAME={SERVICE_NAME}
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=development

# Application port (exposed to host)
PORT={APP_PORT}

# ==============================================================================
# Database Configuration (PostgreSQL)
# ==============================================================================
# Database connection string
DATABASE_URL=postgresql://postgres:postgres@localhost:{DB_PORT}/{DB_NAME}

# Individual components (for flexibility)
DB_HOST=localhost
DB_PORT={DB_PORT}
DB_NAME={DB_NAME}
DB_USER=postgres
DB_PASSWORD=postgres

# Connection pool settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_ECHO=false

# ==============================================================================
# Redis Configuration
# ==============================================================================
REDIS_URL=redis://localhost:{REDIS_PORT}/0
REDIS_HOST=localhost
REDIS_PORT={REDIS_PORT}
REDIS_DB=0
REDIS_PASSWORD=
REDIS_MAX_CONNECTIONS=50

# ==============================================================================
# Security Configuration
# ==============================================================================
# JWT Secret (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Password hashing
PASSWORD_MIN_LENGTH=8
PASSWORD_HASH_ALGORITHM=bcrypt

# ==============================================================================
# CORS Configuration
# ==============================================================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,PATCH,OPTIONS
CORS_ALLOW_HEADERS=*

# ==============================================================================
# Rate Limiting
# ==============================================================================
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# ==============================================================================
# Service Discovery (Consul)
# ==============================================================================
CONSUL_HOST=localhost
CONSUL_PORT=8500
SERVICE_DISCOVERY_ENABLED=false

# ==============================================================================
# External Services URLs (for inter-service communication)
# ==============================================================================
# API Gateway
API_GATEWAY_URL=http://localhost:8003

# Auth Service  
AUTH_SERVICE_URL=http://localhost:8005

# User Service
USER_SERVICE_URL=http://localhost:8006

# Notification Service
NOTIFICATION_SERVICE_URL=http://localhost:8007

# ==============================================================================
# Monitoring & Observability
# ==============================================================================
# Prometheus metrics
METRICS_ENABLED=true
METRICS_PORT=9090

# Jaeger tracing
TRACING_ENABLED=false
JAEGER_HOST=localhost
JAEGER_PORT=6831

# ==============================================================================
# Testing Configuration
# ==============================================================================
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test_{DB_NAME}
TEST_REDIS_URL=redis://localhost:6379/15

# ==============================================================================
# Service-Specific Configuration
# ==============================================================================
{SERVICE_SPECIFIC}
"@

# Service-specific configurations
$serviceSpecificConfigs = @{
    "05-auth-service"         = @"
# OAuth2 Providers
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Session configuration
SESSION_COOKIE_NAME=session_id
SESSION_EXPIRE_SECONDS=3600
"@
    "07-notification-service" = @"
# Email provider
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS provider  
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890

# Push notifications
FCM_SERVER_KEY=your-fcm-server-key
"@
    "08-email-service"        = @"
# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_NAME=GravityWaves
SMTP_FROM_EMAIL=noreply@gravitywaves.com

# SendGrid (alternative)
SENDGRID_API_KEY=your-sendgrid-api-key

# Email templates
TEMPLATE_DIR=app/templates/email
"@
    "09-sms-service"          = @"
# Twilio Configuration
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Alternative: AWS SNS
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
"@
    "10-file-storage-service" = @"
# Storage Configuration
STORAGE_BACKEND=local
STORAGE_PATH=./uploads

# S3 Configuration (if using S3)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1

# File upload limits
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx
"@
}

$created = 0
$updated = 0
$skipped = 0

foreach ($serviceDir in $services) {
    $serviceName = $serviceDir.Name
    $servicePath = $serviceDir.FullName
    
    if (-not (Test-Path $servicePath)) {
        Write-Warn "⚠️  Service not found: $serviceName"
        continue
    }
    
    $envPath = Join-Path $servicePath ".env.example"
    $ports = Get-ServicePorts $serviceName
    
    if (-not $ports) {
        Write-Warn "⚠️  Could not determine ports for $serviceName"
        continue
    }
    
    Write-Info "`n📦 Processing: $serviceName"
    Write-Info "   Ports: App=$($ports.App) | DB=$($ports.DB) | Redis=$($ports.Redis)"
    
    # Get service-specific config
    $serviceSpecific = $serviceSpecificConfigs[$serviceName]
    if (-not $serviceSpecific) {
        $serviceSpecific = "# No service-specific configuration needed"
    }
    
    # Generate database name
    $dbName = $serviceName -replace '^\d{2}-', '' -replace '-', '_'
    
    # Generate .env content
    $envContent = $envTemplate `
        -replace '{SERVICE_NAME}', $serviceName `
        -replace '{APP_PORT}', $ports.App `
        -replace '{DB_PORT}', $ports.DB `
        -replace '{REDIS_PORT}', $ports.Redis `
        -replace '{DB_NAME}', $dbName `
        -replace '{SERVICE_SPECIFIC}', $serviceSpecific
    
    # Check if .env.example exists
    if (Test-Path $envPath) {
        Write-Warn "  ⚠️  .env.example already exists"
        
        if (-not $DryRun) {
            # Backup existing file
            $backupPath = "$envPath.backup"
            Copy-Item $envPath $backupPath
            Write-Info "  💾 Backup created: .env.example.backup"
            
            # Write new file
            Set-Content -Path $envPath -Value $envContent -NoNewline
            Write-Success "  ✅ .env.example updated"
            $updated++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would update .env.example"
        }
    }
    else {
        if (-not $DryRun) {
            Set-Content -Path $envPath -Value $envContent -NoNewline
            Write-Success "  ✅ .env.example created"
            $created++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would create .env.example"
        }
    }
}

Write-Info "`n============================================================"
Write-Info "📊 Summary:"
Write-Success "  ✅ Created: $created"
Write-Success "  📝 Updated: $updated"
Write-Info "  ⏭️  Skipped: $skipped"
Write-Info "  📦 Range: $StartFrom-$EndAt"
Write-Info "  📦 Total: $($services.Count)"
Write-Info "============================================================"

if ($DryRun) {
    Write-Warn "`n⚠️  DRY RUN MODE - No files were modified"
    Write-Info "Run without -DryRun to apply changes"
}

Write-Info "`n💡 Next Steps:"
Write-Info "  1. Copy .env.example to .env in each service"
Write-Info "  2. Update values in .env with actual credentials"
Write-Info "  3. Never commit .env file to git!"
Write-Info "  4. Use secrets management in production"
