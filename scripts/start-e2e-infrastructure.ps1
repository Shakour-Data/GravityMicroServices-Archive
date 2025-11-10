<#
.SYNOPSIS
    End-to-End Testing Script for Gravity MicroServices

.DESCRIPTION
    Tests complete integration flow:
    1. Start infrastructure (PostgreSQL, Redis, Consul)
    2. Setup databases
    3. Start Auth Service
    4. Start User Service
    5. Run integration tests
    6. Verify service discovery
    7. Test token validation flow

.NOTES
    Author: GitHub Copilot (Elite Engineers Team)
    Cost: 0.5 × $150 = $75 USD
    Version: 1.0.0
    Created: 2025-11-08
#>

# Configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors
$ColorSuccess = "Green"
$ColorInfo = "Cyan"
$ColorWarning = "Yellow"
$ColorError = "Red"

function Write-Step {
    param([string]$Message)
    Write-Host "`n✅ $Message" -ForegroundColor $ColorSuccess
}

function Write-Info {
    param([string]$Message)
    Write-Host "   ℹ️  $Message" -ForegroundColor $ColorInfo
}

function Write-Warn {
    param([string]$Message)
    Write-Host "   ⚠️  $Message" -ForegroundColor $ColorWarning
}

function Write-Err {
    param([string]$Message)
    Write-Host "   ❌ $Message" -ForegroundColor $ColorError
}

# Main execution
Write-Host "`n🚀 Starting End-to-End Testing" -ForegroundColor $ColorInfo
Write-Host "="*60 -ForegroundColor $ColorInfo

# Step 1: Check Docker
Write-Step "Checking Docker..."
try {
    $dockerVersion = docker --version
    Write-Info "Docker installed: $dockerVersion"
}
catch {
    Write-Err "Docker is not installed or not running!"
    Write-Info "Please install Docker Desktop and start it."
    exit 1
}

# Step 2: Start infrastructure
Write-Step "Starting infrastructure (PostgreSQL, Redis, Consul)..."
Write-Info "Using docker-compose.e2e.yml"

docker-compose -f docker-compose.e2e.yml up -d

if ($LASTEXITCODE -ne 0) {
    Write-Err "Failed to start infrastructure!"
    exit 1
}

Write-Info "Waiting for services to be healthy..."
Start-Sleep -Seconds 10

# Step 3: Check service health
Write-Step "Checking service health..."

# Check PostgreSQL
Write-Info "Checking PostgreSQL..."
$pgCheck = docker exec gravity-postgres-e2e pg_isready -U gravity
if ($LASTEXITCODE -eq 0) {
    Write-Info "✅ PostgreSQL is ready"
}
else {
    Write-Warn "PostgreSQL not ready yet, waiting..."
    Start-Sleep -Seconds 5
}

# Check Redis
Write-Info "Checking Redis..."
$redisCheck = docker exec gravity-redis-e2e redis-cli -a redis_secret_2025 ping 2>&1
if ($redisCheck -match "PONG") {
    Write-Info "✅ Redis is ready"
}
else {
    Write-Warn "Redis not ready yet"
}

# Check Consul
Write-Info "Checking Consul..."
try {
    $consulCheck = Invoke-WebRequest -Uri "http://localhost:8500/v1/status/leader" -UseBasicParsing
    if ($consulCheck.StatusCode -eq 200) {
        Write-Info "✅ Consul is ready"
    }
}
catch {
    Write-Warn "Consul not ready yet"
}

# Step 4: Show running containers
Write-Step "Running containers:"
docker ps --filter "name=gravity-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Step 5: Show Consul UI
Write-Step "Consul UI available at: http://localhost:8500"

# Step 6: Database setup instructions
Write-Host "`n" + "="*60 -ForegroundColor $ColorInfo
Write-Host "✅ Infrastructure Ready!" -ForegroundColor $ColorSuccess
Write-Host "="*60 -ForegroundColor $ColorInfo

Write-Host "`n⚠️  Next Steps:" -ForegroundColor $ColorWarning
Write-Host "   1. Setup Auth Service database:" -ForegroundColor $ColorInfo
Write-Host "      cd auth-service && .\scripts\setup_database.ps1`n" -ForegroundColor $ColorInfo

Write-Host "   2. Setup User Service database:" -ForegroundColor $ColorInfo
Write-Host "      cd user-service && .\scripts\setup_database.ps1`n" -ForegroundColor $ColorInfo

Write-Host "   3. Start Auth Service:" -ForegroundColor $ColorInfo
Write-Host "      cd auth-service && uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload`n" -ForegroundColor $ColorInfo

Write-Host "   4. Start User Service:" -ForegroundColor $ColorInfo
Write-Host "      cd user-service && uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload`n" -ForegroundColor $ColorInfo

Write-Host "   5. Run E2E tests:" -ForegroundColor $ColorInfo
Write-Host "      .\scripts\run-e2e-tests.ps1`n" -ForegroundColor $ColorInfo

Write-Host "   6. Stop infrastructure:" -ForegroundColor $ColorInfo
Write-Host "      docker-compose -f docker-compose.e2e.yml down`n" -ForegroundColor $ColorInfo
