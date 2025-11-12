#!/usr/bin/env pwsh
# ================================================================================
# Create Standard Dockerfiles for All 52 Microservices
# ================================================================================
# This script generates standardized Dockerfiles following TEAM_PROMPT standards
# - Python 3.11+ base image
# - Multi-stage build for optimization
# - Non-root user for security
# - Health check endpoint
# - .dockerignore for optimization
# ================================================================================

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

# Color functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warn { Write-Host $args -ForegroundColor Yellow }
function Write-Fail { Write-Host $args -ForegroundColor Red }

Write-Info "🐳 Creating Standard Dockerfiles for All 52 Microservices"
Write-Info "============================================================"

# Get all service directories
$services = Get-ChildItem -Directory | Where-Object { $_.Name -match '^\d{2}-' } | Sort-Object Name

Write-Info "📊 Found $($services.Count) microservices"

# Standard Dockerfile template
$dockerfileTemplate = @"
# ================================================================================
# Multi-stage Dockerfile for {SERVICE_NAME}
# ================================================================================
# Following Gravity MicroServices standards from TEAM_PROMPT.md
# - Python 3.11+ for latest features
# - Multi-stage build for smaller image size
# - Non-root user for security
# - Health check for container orchestration
# ================================================================================

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# ================================================================================
# Stage 2: Runtime
# ================================================================================
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port (default 8000, override via PORT env var)
EXPOSE 8000

# Health check endpoint (must be implemented in app)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "app.main"]
"@

# Standard .dockerignore template
$dockerignoreTemplate = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
env/
venv/
ENV/
.venv/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
*.cover

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Git
.git/
.gitignore

# Documentation
*.md
docs/

# CI/CD
.github/

# Environment
.env
.env.*
!.env.example

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Build
build/
dist/
*.egg-info/
"@

$created = 0
$updated = 0
$skipped = 0

foreach ($service in $services) {
    $serviceName = $service.Name
    $servicePath = $service.FullName
    $dockerfilePath = Join-Path $servicePath "Dockerfile"
    $dockerignorePath = Join-Path $servicePath ".dockerignore"
    
    Write-Info "`n📦 Processing: $serviceName"
    
    # Generate Dockerfile content
    $dockerfileContent = $dockerfileTemplate -replace '{SERVICE_NAME}', $serviceName
    
    # Check if Dockerfile exists
    if (Test-Path $dockerfilePath) {
        Write-Warn "  ⚠️  Dockerfile already exists"
        $currentContent = Get-Content $dockerfilePath -Raw
        
        # Check if it's already a multi-stage build
        if ($currentContent -match 'FROM.*as builder' -and $currentContent -match 'FROM.*as runtime') {
            Write-Success "  ✅ Already has multi-stage build - Skipping"
            $skipped++
        }
        else {
            Write-Warn "  📝 Needs update to multi-stage build"
            if (-not $DryRun) {
                # Backup old Dockerfile
                $backupPath = "$dockerfilePath.backup"
                Copy-Item $dockerfilePath $backupPath
                Write-Info "  💾 Backup created: Dockerfile.backup"
                
                # Write new Dockerfile
                Set-Content -Path $dockerfilePath -Value $dockerfileContent -NoNewline
                Write-Success "  ✅ Dockerfile updated"
                $updated++
            }
            else {
                Write-Info "  🔍 [DRY RUN] Would update Dockerfile"
            }
        }
    }
    else {
        Write-Warn "  ⚠️  Dockerfile missing"
        if (-not $DryRun) {
            Set-Content -Path $dockerfilePath -Value $dockerfileContent -NoNewline
            Write-Success "  ✅ Dockerfile created"
            $created++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would create Dockerfile"
        }
    }
    
    # Create/update .dockerignore
    if (-not (Test-Path $dockerignorePath)) {
        if (-not $DryRun) {
            Set-Content -Path $dockerignorePath -Value $dockerignoreTemplate -NoNewline
            Write-Success "  ✅ .dockerignore created"
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would create .dockerignore"
        }
    }
}

Write-Info "`n============================================================"
Write-Info "📊 Summary:"
Write-Success "  ✅ Created: $created"
Write-Success "  📝 Updated: $updated"
Write-Info "  ⏭️  Skipped: $skipped"
Write-Info "  📦 Total: $($services.Count)"
Write-Info "============================================================"

if ($DryRun) {
    Write-Warn "`n⚠️  DRY RUN MODE - No files were modified"
    Write-Info "Run without -DryRun to apply changes"
}
