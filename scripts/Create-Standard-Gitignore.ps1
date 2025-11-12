#!/usr/bin/env pwsh
# ================================================================================
# Create Standard .gitignore for All 52 Services
# ================================================================================
# This script generates standardized .gitignore files for all microservices
# following TEAM_PROMPT.md standards
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

Write-Info "⚙️  Creating Standard .gitignore for Services $StartFrom-$EndAt"
Write-Info "================================================================"

# Standard .gitignore template for microservices
$gitignoreTemplate = @'
# ================================================================================
# {SERVICE_NAME} - Git Ignore Configuration
# ================================================================================
# Gravity MicroServices Platform
# ================================================================================

# ================================================================================
# Python
# ================================================================================

# Byte-compiled / optimized
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environments
venv/
env/
ENV/
.venv/
env.bak/
venv.bak/
.python-version

# Distribution / packaging
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
.ruff_cache/

# ================================================================================
# IDEs and Editors
# ================================================================================

# VS Code
.vscode/
!.vscode/settings.json.example
*.code-workspace

# PyCharm
.idea/
*.iml
*.iws

# Vim
*.swp
*.swo
*~

# Sublime Text
*.sublime-project
*.sublime-workspace

# ================================================================================
# Operating System
# ================================================================================

# macOS
.DS_Store
.AppleDouble
.LSOverride
._*

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/
*.lnk

# Linux
*~
.directory
.Trash-*

# ================================================================================
# Database
# ================================================================================

# SQLite
*.db
*.sqlite
*.sqlite3
*.sql.backup

# PostgreSQL
pgdata/
postgres-data/

# Redis
dump.rdb

# ================================================================================
# Docker
# ================================================================================

docker-compose.override.yml
docker-compose.local.yml

# ================================================================================
# Environment & Secrets
# ================================================================================

# Environment files (NEVER commit real .env!)
.env
.env.*
!.env.example
.env.local
.env.development
.env.test
.env.production

# Secrets
secrets/
credentials/
*.pem
*.key
*.crt
*.cer
*.p12
*.pfx
service-account.json

# ================================================================================
# Logs and Temp
# ================================================================================

# Logs
logs/
*.log
*.log.*
log/

# Temporary files
tmp/
temp/
cache/
*.tmp
*.temp
*.bak
*.backup
*.old
*.orig

# Backup files from scripts
*.py.backup
*.yaml.backup
*.yml.backup
*.json.backup
*.toml.backup
*.md.backup
config.py.backup

# ================================================================================
# Application Specific
# ================================================================================

# Uploads and media
uploads/
media/
static/collected_static/

# Data directories
data/

# Backups
backups/

# Alembic
alembic/versions/__pycache__/

# ================================================================================
# CI/CD
# ================================================================================

# GitHub Actions
.github/workflows/*.log

# ================================================================================
# Kubernetes
# ================================================================================

k8s/secrets/
k8s/*.secret.yaml
k8s/*-secret.yaml

# ================================================================================
# Keep These Files (Explicitly NOT ignored)
# ================================================================================

!.env.example
!.vscode/settings.json.example
!config.example.py
!README.md
!LICENSE
!CHANGELOG.md
!CONTRIBUTING.md
!docs/**/*.md
'@

$created = 0
$updated = 0
$skipped = 0

# Get all service directories
$services = Get-ChildItem -Directory | Where-Object { $_.Name -match '^\d{2}-.*-service$' } | Sort-Object Name

foreach ($service in $services) {
    # Extract service number
    if ($service.Name -match '^(\d{2})-') {
        $serviceNum = [int]$matches[1]
        
        # Skip if outside range
        if ($serviceNum -lt $StartFrom -or $serviceNum -gt $EndAt) {
            continue
        }
    }
    
    $serviceName = $service.Name
    $gitignorePath = Join-Path $service.FullName ".gitignore"
    
    Write-Info "`n📦 Processing: $serviceName"
    
    # Generate .gitignore content
    $gitignoreContent = $gitignoreTemplate -replace '{SERVICE_NAME}', $serviceName
    
    # Check if .gitignore exists
    if (Test-Path $gitignorePath) {
        $existingContent = Get-Content $gitignorePath -Raw
        
        # Check if already comprehensive (has sections and > 100 lines)
        if ($existingContent -match '# ================================================================================\r?\n# Python' -and 
            $existingContent -match '\.backup' -and
            $existingContent.Split("`n").Count -gt 100) {
            Write-Success "  ✅ .gitignore already comprehensive - skipped"
            $skipped++
            continue
        }
        
        Write-Warn "  ⚠️  Existing .gitignore found (not comprehensive)"
        
        if (-not $DryRun) {
            # Backup existing file
            $backupPath = "$gitignorePath.backup"
            Copy-Item $gitignorePath $backupPath -Force
            Write-Info "  💾 Backup created: .gitignore.backup"
            
            # Write new file
            Set-Content -Path $gitignorePath -Value $gitignoreContent -NoNewline
            Write-Success "  ✅ .gitignore updated"
            $updated++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would update .gitignore"
        }
    }
    else {
        Write-Warn "  ⚠️  .gitignore not found"
        
        if (-not $DryRun) {
            Set-Content -Path $gitignorePath -Value $gitignoreContent -NoNewline
            Write-Success "  ✅ .gitignore created"
            $created++
        }
        else {
            Write-Info "  🔍 [DRY RUN] Would create .gitignore"
        }
    }
}

Write-Info "`n================================================================"
Write-Info "📊 Summary:"
Write-Success "  ✅ Created: $created"
Write-Success "  📝 Updated: $updated"
Write-Info "  ⏭️  Skipped: $skipped (already comprehensive)"
Write-Info "  📦 Range: $StartFrom-$EndAt"
Write-Info "================================================================"

if ($DryRun) {
    Write-Warn "`n⚠️  DRY RUN MODE - No files were modified"
    Write-Info "Run without -DryRun to apply changes"
}

Write-Info "`n💡 Next Steps:"
Write-Info "  1. Verify .gitignore files are working"
Write-Info "  2. Check git status to ensure .backup files are ignored"
Write-Info "  3. Commit changes to repository"
