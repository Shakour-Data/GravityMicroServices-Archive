#!/usr/bin/env pwsh
# ================================================================================
# Create Standard docker-compose.yml for All 52 Microservices
# ================================================================================
# This script generates standardized docker-compose.yml files
# - Database container (PostgreSQL)
# - Redis container  
# - Service container
# - Environment variables from .env
# - Health checks
# - Network configuration
# ================================================================================

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

# Color functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }

Write-Info "🐳 Creating Standard docker-compose.yml for All 52 Microservices"
Write-Info "=================================================================="

# Get all service directories
$services = Get-ChildItem -Directory | Where-Object { $_.Name -match '^\d{2}-' } | Sort-Object Name

Write-Info "📊 Found $($services.Count) microservices"

# Standard docker-compose template
$composeTemplate = @"
# ================================================================================
# Docker Compose Configuration for {SERVICE_NAME}
# ================================================================================
# Following Gravity MicroServices standards from TEAM_PROMPT.md
# - Service independence (own database, own Redis)
# - Environment-based configuration
# - Health checks for all services
# - Named volumes for persistence
# ================================================================================

version: '3.8'

services:
  # ==============================================================================
  # PostgreSQL Database
  # ==============================================================================
  db:
    image: postgres:16-alpine
    container_name: {SERVICE_NAME}-db
    environment:
      POSTGRES_DB: `${DB_NAME:-{SERVICE_DB}}
      POSTGRES_USER: `${DB_USER:-postgres}
      POSTGRES_PASSWORD: `${DB_PASSWORD:-postgres}
    ports:
      - "`${DB_PORT:-{DB_PORT}}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - {SERVICE_NETWORK}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U `${DB_USER:-postgres}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ==============================================================================
  # Redis Cache
  # ==============================================================================
  redis:
    image: redis:7-alpine
    container_name: {SERVICE_NAME}-redis
    ports:
      - "`${REDIS_PORT:-{REDIS_PORT}}:6379"
    volumes:
      - redis_data:/data
    networks:
      - {SERVICE_NETWORK}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  # ==============================================================================
  # Application Service
  # ==============================================================================
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: {SERVICE_NAME}-app
    environment:
      # Database
      DATABASE_URL: postgresql://`${DB_USER:-postgres}:`${DB_PASSWORD:-postgres}@db:5432/`${DB_NAME:-{SERVICE_DB}}
      
      # Redis
      REDIS_URL: redis://redis:6379/0
      
      # Application
      APP_NAME: {SERVICE_NAME}
      DEBUG: `${DEBUG:-false}
      LOG_LEVEL: `${LOG_LEVEL:-INFO}
      
      # Port
      PORT: `${APP_PORT:-8000}
    ports:
      - "`${APP_PORT:-{APP_PORT}}:8000"
    volumes:
      - ./app:/app/app:ro
    networks:
      - {SERVICE_NETWORK}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

# ==============================================================================
# Networks
# ==============================================================================
networks:
  {SERVICE_NETWORK}:
    driver: bridge
    name: {SERVICE_NAME}-network

# ==============================================================================
# Volumes
# ==============================================================================
volumes:
  postgres_data:
    name: {SERVICE_NAME}-postgres-data
  redis_data:
    name: {SERVICE_NAME}-redis-data
"@

$created = 0
$updated = 0
$skipped = 0

# Port assignment map (starting from 5432 for DB, 6379 for Redis, 8000+ for apps)
$portCounter = 8000

foreach ($service in $services) {
    $serviceName = $service.Name
    $servicePath = $service.FullName
    $composePath = Join-Path $servicePath "docker-compose.yml"
    
    # Extract number from service name
    if ($serviceName -match '^(\d{2})-(.+)$') {
        $serviceNumber = $matches[1]
        $shortName = $matches[2]
    }
    
    # Calculate ports
    $dbPort = 5400 + [int]$serviceNumber
    $redisPort = 6300 + [int]$serviceNumber
    $appPort = 8000 + [int]$serviceNumber
    
    # Service-specific values
    $serviceDb = $shortName -replace '-service', '' -replace '-', '_'
    $serviceNetwork = "$shortName-net"
    
    Write-Info "`n📦 Processing: $serviceName"
    Write-Info "   DB Port: $dbPort | Redis Port: $redisPort | App Port: $appPort"
    
    # Generate docker-compose content
    $composeContent = $composeTemplate `
        -replace '{SERVICE_NAME}', $serviceName `
        -replace '{SERVICE_DB}', $serviceDb `
        -replace '{SERVICE_NETWORK}', $serviceNetwork `
        -replace '{DB_PORT}', $dbPort `
        -replace '{REDIS_PORT}', $redisPort `
        -replace '{APP_PORT}', $appPort
    
    # Check if docker-compose.yml exists
    if (Test-Path $composePath) {
        $currentContent = Get-Content $composePath -Raw
        
        # Check if it has all required services
        $hasDb = $currentContent -match 'postgres'
        $hasRedis = $currentContent -match 'redis'
        $hasHealthChecks = $currentContent -match 'healthcheck'
        
        if ($hasDb -and $hasRedis -and $hasHealthChecks) {
            Write-Success "  ✅ Already complete - Skipping"
            $skipped++
        }
        else {
            Write-Warn "  📝 Needs update"
            if (-not $DryRun) {
                # Backup
                $backupPath = "$composePath.backup"
                Copy-Item $composePath $backupPath
                Write-Info "  💾 Backup created: docker-compose.yml.backup"
                
                # Write new compose file
                Set-Content -Path $composePath -Value $composeContent -NoNewline
                Write-Success "  ✅ docker-compose.yml updated"
                $updated++
            }
            else {
                Write-Info "  🔍 [DRY RUN] Would update docker-compose.yml"
            }
        }
    }
    else {
        Write-Warn "  ⚠️  docker-compose.yml missing"
        if (-not $DryRun) {
            Set-Content -Path $composePath -Value $composeContent -NoNewline
            Write-Success "  ✅ docker-compose.yml created"
            $created++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would create docker-compose.yml"
        }
    }
}

Write-Info "`n=================================================================="
Write-Info "📊 Summary:"
Write-Success "  ✅ Created: $created"
Write-Success "  📝 Updated: $updated"
Write-Info "  ⏭️  Skipped: $skipped"
Write-Info "  📦 Total: $($services.Count)"
Write-Info "=================================================================="

if ($DryRun) {
    Write-Warn "`n⚠️  DRY RUN MODE - No files were modified"
    Write-Info "Run without -DryRun to apply changes"
}

Write-Info "`n📝 Port Allocation Summary:"
Write-Info "   Databases: 5401-5452 (PostgreSQL)"
Write-Info "   Redis: 6301-6352"
Write-Info "   Applications: 8001-8052"
