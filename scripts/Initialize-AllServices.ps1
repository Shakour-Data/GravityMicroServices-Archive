<#
.SYNOPSIS
    Initialize all 52 Gravity microservices with complete boilerplate code.

.DESCRIPTION
    This script automatically creates directory structures and boilerplate files 
    for all 52 Gravity microservices based on the numbered service list.
    Each service gets a complete, ready-to-develop structure.

.PARAMETER ServicesPath
    Base path where services will be created. Default: current directory.

.PARAMETER StartFrom
    Service number to start from (1-52). Default: 1.

.PARAMETER EndAt
    Service number to end at (1-52). Default: 52.

.EXAMPLE
    .\Initialize-AllServices.ps1
    Creates all 52 services in current directory

.EXAMPLE
    .\Initialize-AllServices.ps1 -ServicesPath "C:\Projects\Gravity" -StartFrom 15 -EndAt 20
    Creates services 15-20 in specified directory
#>

param(
    [string]$ServicesPath = ".",
    [int]$StartFrom = 1,
    [int]$EndAt = 52
)

# Service definitions array (all 52 services)
$services = @(
    @{Number = "01"; Name = "common-library"; Port = "N/A"; Database = "None"; Description = "Shared utilities and base models" },
    @{Number = "02"; Name = "service-discovery"; Port = "8500"; Database = "None"; Description = "Service registry with Consul" },
    @{Number = "03"; Name = "api-gateway"; Port = "8000"; Database = "Redis"; Description = "Single entry point with routing and rate limiting" },
    @{Number = "04"; Name = "config-service"; Port = "8090"; Database = "PostgreSQL"; Description = "Centralized configuration management" },
    @{Number = "05"; Name = "auth-service"; Port = "8081"; Database = "PostgreSQL"; Description = "OAuth2 authentication with JWT and MFA" },
    @{Number = "06"; Name = "user-service"; Port = "8082"; Database = "PostgreSQL"; Description = "User profiles and account management" },
    @{Number = "07"; Name = "notification-service"; Port = "8085"; Database = "PostgreSQL"; Description = "Multi-channel notifications" },
    @{Number = "08"; Name = "email-service"; Port = "8086"; Database = "PostgreSQL"; Description = "Dedicated email service with templates" },
    @{Number = "09"; Name = "sms-service"; Port = "8087"; Database = "PostgreSQL"; Description = "SMS delivery via Twilio/AWS SNS" },
    @{Number = "10"; Name = "file-storage-service"; Port = "8088"; Database = "PostgreSQL+S3"; Description = "File upload with CDN integration" },
    @{Number = "11"; Name = "permission-service"; Port = "8083"; Database = "PostgreSQL"; Description = "Fine-grained permissions and ACL" },
    @{Number = "12"; Name = "session-service"; Port = "8084"; Database = "Redis"; Description = "Session management and device tracking" },
    @{Number = "13"; Name = "audit-log-service"; Port = "8089"; Database = "PostgreSQL"; Description = "Comprehensive audit logging" },
    @{Number = "14"; Name = "cache-service"; Port = "8091"; Database = "Redis"; Description = "Distributed caching layer" },
    @{Number = "15"; Name = "payment-service"; Port = "8100"; Database = "PostgreSQL"; Description = "Payment gateway integration" },
    @{Number = "16"; Name = "order-service"; Port = "8101"; Database = "PostgreSQL"; Description = "Order lifecycle management" },
    @{Number = "17"; Name = "product-service"; Port = "8102"; Database = "PostgreSQL"; Description = "Product catalog and inventory" },
    @{Number = "18"; Name = "cart-service"; Port = "8103"; Database = "Redis+PostgreSQL"; Description = "Shopping cart with persistence" },
    @{Number = "19"; Name = "search-service"; Port = "8104"; Database = "ElasticSearch"; Description = "Full-text search with filters" },
    @{Number = "20"; Name = "recommendation-service"; Port = "8105"; Database = "PostgreSQL+Redis"; Description = "Personalized recommendations" },
    @{Number = "21"; Name = "review-service"; Port = "8106"; Database = "PostgreSQL"; Description = "Product reviews and ratings" },
    @{Number = "22"; Name = "wishlist-service"; Port = "8107"; Database = "PostgreSQL"; Description = "User wishlists and collections" },
    @{Number = "23"; Name = "analytics-service"; Port = "8108"; Database = "ClickHouse"; Description = "Real-time analytics and metrics" },
    @{Number = "24"; Name = "reporting-service"; Port = "8109"; Database = "PostgreSQL"; Description = "Report generation and export" },
    @{Number = "25"; Name = "inventory-service"; Port = "8110"; Database = "PostgreSQL"; Description = "Stock management and tracking" },
    @{Number = "26"; Name = "shipping-service"; Port = "8111"; Database = "PostgreSQL"; Description = "Shipping calculation and tracking" },
    @{Number = "27"; Name = "invoice-service"; Port = "8112"; Database = "PostgreSQL"; Description = "Invoice generation and tax calculation" },
    @{Number = "28"; Name = "chat-service"; Port = "8120"; Database = "PostgreSQL+Redis"; Description = "Real-time messaging with WebSocket" },
    @{Number = "29"; Name = "video-call-service"; Port = "8121"; Database = "PostgreSQL"; Description = "WebRTC video calls" },
    @{Number = "30"; Name = "geolocation-service"; Port = "8122"; Database = "PostgreSQL+PostGIS"; Description = "Location tracking and geofencing" },
    @{Number = "31"; Name = "subscription-service"; Port = "8123"; Database = "PostgreSQL"; Description = "Recurring billing management" },
    @{Number = "32"; Name = "loyalty-service"; Port = "8124"; Database = "PostgreSQL"; Description = "Loyalty points and rewards" },
    @{Number = "33"; Name = "coupon-service"; Port = "8125"; Database = "PostgreSQL"; Description = "Coupon management and validation" },
    @{Number = "34"; Name = "referral-service"; Port = "8126"; Database = "PostgreSQL"; Description = "Referral program tracking" },
    @{Number = "35"; Name = "translation-service"; Port = "8127"; Database = "PostgreSQL+Redis"; Description = "Multi-language support" },
    @{Number = "36"; Name = "cms-service"; Port = "8128"; Database = "PostgreSQL"; Description = "Content management system" },
    @{Number = "37"; Name = "feedback-service"; Port = "8129"; Database = "PostgreSQL"; Description = "User feedback and bug reports" },
    @{Number = "38"; Name = "monitoring-service"; Port = "8140"; Database = "InfluxDB"; Description = "Service health monitoring" },
    @{Number = "39"; Name = "logging-service"; Port = "8141"; Database = "ElasticSearch"; Description = "Centralized log aggregation" },
    @{Number = "40"; Name = "scheduler-service"; Port = "8142"; Database = "PostgreSQL+Redis"; Description = "Job scheduling and background tasks" },
    @{Number = "41"; Name = "webhook-service"; Port = "8143"; Database = "PostgreSQL"; Description = "Webhook management and delivery" },
    @{Number = "42"; Name = "export-service"; Port = "8144"; Database = "PostgreSQL"; Description = "Data export in multiple formats" },
    @{Number = "43"; Name = "import-service"; Port = "8145"; Database = "PostgreSQL"; Description = "Bulk data import with validation" },
    @{Number = "44"; Name = "backup-service"; Port = "8146"; Database = "PostgreSQL+S3"; Description = "Automated backup and restore" },
    @{Number = "45"; Name = "rate-limiter-service"; Port = "8147"; Database = "Redis"; Description = "Distributed rate limiting" },
    @{Number = "46"; Name = "ab-testing-service"; Port = "8148"; Database = "PostgreSQL"; Description = "A/B test management" },
    @{Number = "47"; Name = "feature-flag-service"; Port = "8149"; Database = "PostgreSQL+Redis"; Description = "Feature toggles and gradual rollout" },
    @{Number = "48"; Name = "tax-service"; Port = "8150"; Database = "PostgreSQL"; Description = "Multi-jurisdiction tax calculation" },
    @{Number = "49"; Name = "fraud-detection-service"; Port = "8151"; Database = "PostgreSQL"; Description = "Fraud detection with ML" },
    @{Number = "50"; Name = "kyc-service"; Port = "8152"; Database = "PostgreSQL"; Description = "KYC verification and compliance" },
    @{Number = "51"; Name = "gamification-service"; Port = "8153"; Database = "PostgreSQL"; Description = "Badges, achievements, leaderboards" },
    @{Number = "52"; Name = "social-media-service"; Port = "8154"; Database = "PostgreSQL"; Description = "Social login and sharing" }
)

function New-ServiceStructure {
    param(
        [hashtable]$Service,
        [string]$BasePath
    )
    
    $serviceName = "$($Service.Number)-$($Service.Name)"
    $servicePath = Join-Path $BasePath $serviceName
    
    Write-Host "Creating $serviceName..." -ForegroundColor Cyan
    
    # Create main directory
    New-Item -ItemType Directory -Path $servicePath -Force | Out-Null
    
    # Create subdirectories
    $directories = @(
        "app",
        "app/api",
        "app/api/v1",
        "app/core",
        "app/models",
        "app/schemas",
        "app/services",
        "alembic",
        "alembic/versions",
        "tests",
        "scripts",
        "k8s",
        ".github",
        ".github/workflows"
    )
    
    foreach ($dir in $directories) {
        $dirPath = Join-Path $servicePath $dir
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
    
    # Create __init__.py files
    $initFiles = @(
        "app/__init__.py",
        "app/api/__init__.py",
        "app/api/v1/__init__.py",
        "app/core/__init__.py",
        "app/models/__init__.py",
        "app/schemas/__init__.py",
        "app/services/__init__.py",
        "tests/__init__.py",
        "scripts/__init__.py"
    )
    
    foreach ($file in $initFiles) {
        $filePath = Join-Path $servicePath $file
        New-Item -ItemType File -Path $filePath -Force | Out-Null
    }
    
    # Create main.py
    $mainPyContent = @"
from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="$($Service.Name.Replace('-', ' ').ToUpper())",
    description="$($Service.Description)",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "$serviceName"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=$($Service.Port), reload=True)
"@
    Set-Content -Path (Join-Path $servicePath "app/main.py") -Value $mainPyContent
    
    # Create config.py
    $configContent = @"
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "$serviceName"
    PORT: int = $($Service.Port)
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
"@
    Set-Content -Path (Join-Path $servicePath "app/config.py") -Value $configContent
    
    # Create README.md
    $readmeContent = @"
# $serviceName

$($Service.Description)

## Quick Start

``````bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port $($Service.Port) --reload
``````

## Port
- **Service Port:** $($Service.Port)

## Database
- **Type:** $($Service.Database)

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:$($Service.Port)/docs
- Redoc: http://localhost:$($Service.Port)/redoc
"@
    Set-Content -Path (Join-Path $servicePath "README.md") -Value $readmeContent
    
    # Create .env.example
    $envContent = @"
SERVICE_NAME=$serviceName
PORT=$($Service.Port)
DEBUG=true
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/$($Service.Name.Replace('-', '_'))_db
REDIS_URL=redis://localhost:6379/0
"@
    Set-Content -Path (Join-Path $servicePath ".env.example") -Value $envContent
    
    # Create .gitignore
    $gitignoreContent = @"
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
.env
*.log
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.DS_Store
"@
    Set-Content -Path (Join-Path $servicePath ".gitignore") -Value $gitignoreContent
    
    Write-Host "✅ Created $serviceName" -ForegroundColor Green
}

# Main execution
Write-Host "🚀 Gravity MicroServices - Service Initialization" -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Creating services $StartFrom to $EndAt in: $ServicesPath" -ForegroundColor Cyan
Write-Host ""

$createdCount = 0
for ($i = $StartFrom - 1; $i -lt $EndAt; $i++) {
    if ($i -lt $services.Count) {
        New-ServiceStructure -Service $services[$i] -BasePath $ServicesPath
        $createdCount++
    }
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Yellow
Write-Host "✅ Successfully created $createdCount services!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review generated services in: $ServicesPath" -ForegroundColor White
Write-Host "2. Customize pyproject.toml for each service" -ForegroundColor White
Write-Host "3. Run 'poetry install' in each service directory" -ForegroundColor White
Write-Host "4. Start development!" -ForegroundColor White
Write-Host ""
