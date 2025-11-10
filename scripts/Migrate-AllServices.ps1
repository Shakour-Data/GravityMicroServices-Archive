<#
.SYNOPSIS
    Migrate all 52 services from monorepo to individual GitHub repositories

.DESCRIPTION
    This script automates the migration of all Gravity microservices from the
    monorepo to individual repositories in the GravityMicroServices organization.

.PARAMETER GitHubToken
    GitHub Personal Access Token with repo and admin:org permissions

.PARAMETER StartFrom
    Service number to start from (default: 1)

.PARAMETER EndAt
    Service number to end at (default: 52)

.PARAMETER DryRun
    If set, shows what would be done without making changes

.PARAMETER Parallel
    Number of parallel migrations (default: 1, max: 5)

.EXAMPLE
    .\Migrate-AllServices.ps1 -GitHubToken "ghp_xxx"

.EXAMPLE
    .\Migrate-AllServices.ps1 -GitHubToken "ghp_xxx" -StartFrom 1 -EndAt 10

.NOTES
    Author: Gravity Elite Engineering Team
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$GitHubToken,

    [Parameter(Mandatory = $false)]
    [int]$StartFrom = 1,

    [Parameter(Mandatory = $false)]
    [int]$EndAt = 52,

    [Parameter(Mandatory = $false)]
    [switch]$DryRun,

    [Parameter(Mandatory = $false)]
    [ValidateRange(1, 5)]
    [int]$Parallel = 1
)

$ErrorActionPreference = "Continue"

# Colors for output
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }

# Service definitions
$Services = @(
    @{Number = "01"; Name = "common-library"; Priority = "P0"; Team = "core-infrastructure" },
    @{Number = "02"; Name = "service-discovery"; Priority = "P0"; Team = "core-infrastructure" },
    @{Number = "03"; Name = "api-gateway"; Priority = "P0"; Team = "core-infrastructure" },
    @{Number = "04"; Name = "config-server"; Priority = "P0"; Team = "core-infrastructure" },
    @{Number = "05"; Name = "auth-service"; Priority = "P1"; Team = "authentication-team" },
    @{Number = "06"; Name = "user-service"; Priority = "P1"; Team = "authentication-team" },
    @{Number = "07"; Name = "notification-service"; Priority = "P1"; Team = "notification-team" },
    @{Number = "08"; Name = "email-service"; Priority = "P1"; Team = "notification-team" },
    @{Number = "09"; Name = "sms-service"; Priority = "P1"; Team = "notification-team" },
    @{Number = "10"; Name = "push-notification-service"; Priority = "P1"; Team = "notification-team" },
    @{Number = "11"; Name = "payment-service"; Priority = "P1"; Team = "payment-team" },
    @{Number = "12"; Name = "order-service"; Priority = "P1"; Team = "payment-team" },
    @{Number = "13"; Name = "product-service"; Priority = "P1"; Team = "payment-team" },
    @{Number = "14"; Name = "inventory-service"; Priority = "P1"; Team = "payment-team" },
    @{Number = "15"; Name = "shipping-service"; Priority = "P2"; Team = "payment-team" },
    @{Number = "16"; Name = "tracking-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "17"; Name = "analytics-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "18"; Name = "reporting-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "19"; Name = "logging-service"; Priority = "P2"; Team = "devops-team" },
    @{Number = "20"; Name = "monitoring-service"; Priority = "P2"; Team = "devops-team" },
    @{Number = "21"; Name = "search-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "22"; Name = "recommendation-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "23"; Name = "review-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "24"; Name = "rating-service"; Priority = "P2"; Team = "data-team" },
    @{Number = "25"; Name = "cart-service"; Priority = "P2"; Team = "payment-team" },
    @{Number = "26"; Name = "wishlist-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "27"; Name = "coupon-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "28"; Name = "loyalty-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "29"; Name = "refund-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "30"; Name = "invoice-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "31"; Name = "tax-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "32"; Name = "pricing-service"; Priority = "P3"; Team = "payment-team" },
    @{Number = "33"; Name = "catalog-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "34"; Name = "media-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "35"; Name = "content-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "36"; Name = "cms-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "37"; Name = "localization-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "38"; Name = "translation-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "39"; Name = "file-storage-service"; Priority = "P3"; Team = "data-team" },
    @{Number = "40"; Name = "backup-service"; Priority = "P3"; Team = "devops-team" },
    @{Number = "41"; Name = "scheduler-service"; Priority = "P3"; Team = "devops-team" },
    @{Number = "42"; Name = "webhook-service"; Priority = "P3"; Team = "core-infrastructure" },
    @{Number = "43"; Name = "audit-service"; Priority = "P3"; Team = "security-team" },
    @{Number = "44"; Name = "compliance-service"; Priority = "P3"; Team = "security-team" },
    @{Number = "45"; Name = "gdpr-service"; Priority = "P4"; Team = "security-team" },
    @{Number = "46"; Name = "chat-service"; Priority = "P4"; Team = "notification-team" },
    @{Number = "47"; Name = "video-call-service"; Priority = "P4"; Team = "notification-team" },
    @{Number = "48"; Name = "geolocation-service"; Priority = "P4"; Team = "data-team" },
    @{Number = "49"; Name = "map-service"; Priority = "P4"; Team = "data-team" },
    @{Number = "50"; Name = "weather-service"; Priority = "P4"; Team = "data-team" },
    @{Number = "51"; Name = "ai-ml-service"; Priority = "P4"; Team = "data-team" },
    @{Number = "52"; Name = "social-media-service"; Priority = "P4"; Team = "data-team" }
)

Write-Info "================================================"
Write-Info "  Gravity Batch Migration Tool"
Write-Info "================================================"
Write-Info ""
Write-Info "Total Services: 52"
Write-Info "Migration Range: $StartFrom to $EndAt"
Write-Info "Parallel Jobs: $Parallel"
Write-Info "Dry Run: $DryRun"
Write-Info ""

# Filter services based on range
$ServicesToMigrate = $Services | Where-Object { 
    [int]$_.Number -ge $StartFrom -and [int]$_.Number -le $EndAt 
}

Write-Info "Services to migrate: $($ServicesToMigrate.Count)"
Write-Info ""

# Create migration directory
$MigrationDir = Join-Path $PSScriptRoot "..\migration"
if (-not (Test-Path $MigrationDir)) {
    New-Item -ItemType Directory -Path $MigrationDir -Force | Out-Null
}

# Initialize log
$LogPath = Join-Path $MigrationDir "migration-log.txt"
$ErrorLogPath = Join-Path $MigrationDir "migration-errors.txt"
$StartTime = Get-Date

"=" * 80 | Out-File $LogPath -Append
"Migration started at: $StartTime" | Out-File $LogPath -Append
"=" * 80 | Out-File $LogPath -Append

# Track statistics
$Stats = @{
    Total   = $ServicesToMigrate.Count
    Success = 0
    Failed  = 0
    Skipped = 0
}

# Migrate services
$Counter = 0
foreach ($service in $ServicesToMigrate) {
    $Counter++
    $Progress = [math]::Round(($Counter / $ServicesToMigrate.Count) * 100, 1)
    
    Write-Host ""
    Write-Host "[$Counter/$($ServicesToMigrate.Count)] " -NoNewline -ForegroundColor Yellow
    Write-Info "Migrating $($service.Number)-$($service.Name) (Priority: $($service.Priority), Team: $($service.Team))"
    Write-Host "Progress: $Progress%" -ForegroundColor Cyan
    
    try {
        # Build migrate command
        $MigrateScript = Join-Path $PSScriptRoot "Migrate-Service.ps1"
        $Arguments = @(
            "-ServiceNumber", $service.Number,
            "-ServiceName", $service.Name,
            "-GitHubToken", $GitHubToken
        )
        
        if ($DryRun) {
            $Arguments += "-DryRun"
        }
        
        # Execute migration
        & $MigrateScript @Arguments
        
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            $Stats.Success++
            Write-Success "Migration successful: $($service.Number)-$($service.Name)"
            
            "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss')) SUCCESS $($service.Number)-$($service.Name)" | Out-File $LogPath -Append
        }
        else {
            $Stats.Failed++
            Write-Error "Migration failed: $($service.Number)-$($service.Name)"
            
            "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss')) FAILED $($service.Number)-$($service.Name)" | Out-File $LogPath -Append
            "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss')) $($service.Number)-$($service.Name): Exit code $LASTEXITCODE" | Out-File $ErrorLogPath -Append
        }
    }
    catch {
        $Stats.Failed++
        Write-Error "Migration error: $($service.Number)-$($service.Name) - $_"
        
        "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss')) ERROR $($service.Number)-$($service.Name)" | Out-File $LogPath -Append
        "$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss')) $($service.Number)-$($service.Name): $_" | Out-File $ErrorLogPath -Append
    }
    
    # Small delay to avoid rate limiting
    Start-Sleep -Seconds 2
}

# Calculate duration
$EndTime = Get-Date
$Duration = $EndTime - $StartTime

# Final report
Write-Host ""
Write-Info "================================================"
Write-Success "  Migration Completed!"
Write-Info "================================================"
Write-Host ""
Write-Host "Statistics:" -ForegroundColor Cyan
Write-Host "  Total Services: $($Stats.Total)" -ForegroundColor White
Write-Host "  Successful: $($Stats.Success)" -ForegroundColor Green
Write-Host "  Failed: $($Stats.Failed)" -ForegroundColor Red
Write-Host "  Skipped: $($Stats.Skipped)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Duration: $($Duration.ToString('hh\:mm\:ss'))" -ForegroundColor Cyan
Write-Host ""
Write-Host "Logs:" -ForegroundColor Cyan
Write-Host "  Migration Log: $LogPath" -ForegroundColor White
if (Test-Path $ErrorLogPath) {
    Write-Host "  Error Log: $ErrorLogPath" -ForegroundColor Red
}
Write-Host ""

# Write final log
"=" * 80 | Out-File $LogPath -Append
"Migration completed at: $EndTime" | Out-File $LogPath -Append
"Duration: $($Duration.ToString('hh\:mm\:ss'))" | Out-File $LogPath -Append
"Success: $($Stats.Success), Failed: $($Stats.Failed), Skipped: $($Stats.Skipped)" | Out-File $LogPath -Append
"=" * 80 | Out-File $LogPath -Append

# Generate summary report
$ReportPath = Join-Path $MigrationDir "migration-summary.md"
@"
# Gravity Services Migration Summary

## Overview
- **Started:** $($StartTime.ToString('yyyy-MM-dd HH:mm:ss'))
- **Completed:** $($EndTime.ToString('yyyy-MM-dd HH:mm:ss'))
- **Duration:** $($Duration.ToString('hh\:mm\:ss'))

## Statistics
- **Total Services:** $($Stats.Total)
- **✓ Successful:** $($Stats.Success)
- **✗ Failed:** $($Stats.Failed)
- **⊘ Skipped:** $($Stats.Skipped)

## Success Rate
**$([math]::Round(($Stats.Success / $Stats.Total) * 100, 1))%**

## Migrated Services
$(
    $ServicesToMigrate | ForEach-Object {
        "- [$($_.Number)-$($_.Name)](https://github.com/GravityMicroServices/gravity-$($_.Name)) - $($_.Priority) - $($_.Team)"
    } | Out-String
)

## Next Steps
1. Verify all repositories are accessible
2. Check CI/CD workflows are running
3. Update team access permissions
4. Archive monorepo
5. Update documentation

---
*Generated by Gravity Migration Tool*
"@ | Out-File $ReportPath

Write-Success "Summary report generated: $ReportPath"

if ($Stats.Failed -gt 0) {
    Write-Warning "Some migrations failed. Please check the error log: $ErrorLogPath"
    exit 1
}

Write-Success "All migrations completed successfully!"
