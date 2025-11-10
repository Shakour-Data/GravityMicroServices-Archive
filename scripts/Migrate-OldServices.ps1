<#
.SYNOPSIS
    Migrate old services to new numbered structure

.DESCRIPTION
    This script automatically migrates code from old service folders
    to new numbered service folders, maintaining all work done.

.PARAMETER DryRun
    Show what would be done without actually doing it

.PARAMETER SkipBackup
    Skip creating backup (not recommended)

.EXAMPLE
    .\Migrate-OldServices.ps1
    Migrates all old services with backup

.EXAMPLE
    .\Migrate-OldServices.ps1 -DryRun
    Shows what would be done without actually doing it
#>

param(
    [switch]$DryRun = $false,
    [switch]$SkipBackup = $false
)

# Service mapping: old name → new name
$serviceMappings = @{
    "common-library"       = "01-common-library"
    "service-discovery"    = "02-service-discovery"
    "api-gateway"          = "03-api-gateway"
    "auth-service"         = "05-auth-service"
    "user-service"         = "06-user-service"
    "notification-service" = "07-notification-service"
}

Write-Host "🔧 Gravity Services Migration Tool" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host ""

if ($DryRun) {
    Write-Host "⚠️  DRY RUN MODE - No changes will be made" -ForegroundColor Cyan
    Write-Host ""
}

# Step 1: Create backup directory
if (-not $SkipBackup -and -not $DryRun) {
    Write-Host "📦 Creating backup directory..." -ForegroundColor Cyan
    if (-not (Test-Path "_OLD_SERVICES_BACKUP")) {
        New-Item -ItemType Directory -Path "_OLD_SERVICES_BACKUP" -Force | Out-Null
        Write-Host "✅ Created _OLD_SERVICES_BACKUP/" -ForegroundColor Green
    }
    else {
        Write-Host "✅ Backup directory already exists" -ForegroundColor Green
    }
    Write-Host ""
}

# Step 2: Migrate each service
$migratedCount = 0
$skippedCount = 0

foreach ($mapping in $serviceMappings.GetEnumerator()) {
    $oldName = $mapping.Key
    $newName = $mapping.Value
    
    Write-Host "🔄 Processing: $oldName → $newName" -ForegroundColor Yellow
    
    # Check if old service exists
    if (-not (Test-Path $oldName)) {
        Write-Host "   ⏭️  Skipped: $oldName not found" -ForegroundColor Gray
        $skippedCount++
        Write-Host ""
        continue
    }
    
    # Check if new service exists
    if (-not (Test-Path $newName)) {
        Write-Host "   ❌ Error: Target $newName not found!" -ForegroundColor Red
        Write-Host ""
        continue
    }
    
    if ($DryRun) {
        Write-Host "   📋 Would migrate:" -ForegroundColor Cyan
        Write-Host "      - app/ code" -ForegroundColor White
        Write-Host "      - tests/" -ForegroundColor White
        Write-Host "      - configuration files" -ForegroundColor White
        Write-Host "      - database migrations" -ForegroundColor White
    }
    else {
        Write-Host "   📦 Backing up $oldName..." -ForegroundColor Cyan
        
        if (-not $SkipBackup) {
            $backupPath = "_OLD_SERVICES_BACKUP/$oldName"
            if (Test-Path $backupPath) {
                Remove-Item -Recurse -Force $backupPath
            }
            Copy-Item -Recurse $oldName $backupPath
            Write-Host "   ✅ Backed up to $backupPath" -ForegroundColor Green
        }
        
        Write-Host "   📂 Migrating files..." -ForegroundColor Cyan
        
        # Migrate app/ directory
        if (Test-Path "$oldName/app") {
            Write-Host "      → app/" -ForegroundColor White
            Copy-Item -Recurse -Force "$oldName/app/*" "$newName/app/"
        }
        
        # Migrate tests/ directory
        if (Test-Path "$oldName/tests") {
            Write-Host "      → tests/" -ForegroundColor White
            Copy-Item -Recurse -Force "$oldName/tests/*" "$newName/tests/"
        }
        
        # Migrate alembic/ directory
        if (Test-Path "$oldName/alembic") {
            Write-Host "      → alembic/" -ForegroundColor White
            if (Test-Path "$oldName/alembic/versions") {
                Copy-Item -Recurse -Force "$oldName/alembic/versions/*" "$newName/alembic/versions/" -ErrorAction SilentlyContinue
            }
            if (Test-Path "$oldName/alembic/env.py") {
                Copy-Item -Force "$oldName/alembic/env.py" "$newName/alembic/"
            }
        }
        
        # Migrate scripts/ directory
        if (Test-Path "$oldName/scripts") {
            Write-Host "      → scripts/" -ForegroundColor White
            Copy-Item -Recurse -Force "$oldName/scripts/*" "$newName/scripts/"
        }
        
        # Migrate configuration files
        $configFiles = @(
            "pyproject.toml",
            "alembic.ini",
            ".env.example",
            "Dockerfile",
            "docker-compose.yml",
            "pytest.ini",
            "coverage.xml"
        )
        
        foreach ($file in $configFiles) {
            if (Test-Path "$oldName/$file") {
                Write-Host "      → $file" -ForegroundColor White
                Copy-Item -Force "$oldName/$file" "$newName/"
            }
        }
        
        # Migrate README if it has content
        if (Test-Path "$oldName/README.md") {
            $oldReadmeSize = (Get-Item "$oldName/README.md").Length
            $newReadmeSize = (Get-Item "$newName/README.md").Length
            
            if ($oldReadmeSize -gt $newReadmeSize) {
                Write-Host "      → README.md (old has more content)" -ForegroundColor White
                Copy-Item -Force "$oldName/README.md" "$newName/"
            }
        }
        
        Write-Host "   ✅ Migration complete!" -ForegroundColor Green
        $migratedCount++
    }
    
    Write-Host ""
}

# Step 3: Rename old directories
if (-not $DryRun -and $migratedCount -gt 0) {
    Write-Host "🗑️  Archiving old service directories..." -ForegroundColor Cyan
    Write-Host ""
    
    foreach ($mapping in $serviceMappings.GetEnumerator()) {
        $oldName = $mapping.Key
        
        if (Test-Path $oldName) {
            $archivedName = "${oldName}.OLD"
            
            if (Test-Path $archivedName) {
                Remove-Item -Recurse -Force $archivedName
            }
            
            Rename-Item $oldName $archivedName
            Write-Host "   ✅ Renamed $oldName → $archivedName" -ForegroundColor Green
        }
    }
    
    Write-Host ""
}

# Summary
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "📊 Migration Summary" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "✅ Migrated: $migratedCount services" -ForegroundColor Green
Write-Host "⏭️  Skipped: $skippedCount services" -ForegroundColor Gray

if (-not $DryRun -and $migratedCount -gt 0) {
    Write-Host ""
    Write-Host "📁 Old services renamed with .OLD suffix" -ForegroundColor Cyan
    Write-Host "📦 Backups available in: _OLD_SERVICES_BACKUP/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✅ Next Steps:" -ForegroundColor Green
    Write-Host "   1. Test each migrated service" -ForegroundColor White
    Write-Host "   2. Verify all functionality works" -ForegroundColor White
    Write-Host "   3. After verification, delete .OLD folders:" -ForegroundColor White
    Write-Host "      Get-ChildItem -Directory -Filter '*.OLD' | Remove-Item -Recurse" -ForegroundColor Gray
    Write-Host ""
}

if ($DryRun) {
    Write-Host ""
    Write-Host "ℹ️  This was a dry run. Run without -DryRun to perform migration." -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "✅ Done!" -ForegroundColor Green
