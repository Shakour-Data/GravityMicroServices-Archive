# ============================================================================
# Script: Update-GitHubWorkflows.ps1
# Purpose: Update GitHub Actions workflows for all microservices
# Author: Gravity Elite Team
# Date: 2024
# ============================================================================

param(
    [int]$StartFrom = 4,
    [int]$EndAt = 52,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Service metadata
$services = @{
    "04" = @{ name = "config-service"; port = 8004 }
    "05" = @{ name = "auth-service"; port = 8005 }
    "06" = @{ name = "user-service"; port = 8006 }
    "07" = @{ name = "notification-service"; port = 8007 }
    "08" = @{ name = "email-service"; port = 8008 }
    "09" = @{ name = "sms-service"; port = 8009 }
    "10" = @{ name = "file-storage-service"; port = 8010 }
    "11" = @{ name = "permission-service"; port = 8011 }
    "12" = @{ name = "session-service"; port = 8012 }
    "13" = @{ name = "audit-log-service"; port = 8013 }
    "14" = @{ name = "cache-service"; port = 8014 }
    "15" = @{ name = "payment-service"; port = 8015 }
    "16" = @{ name = "order-service"; port = 8016 }
    "17" = @{ name = "product-service"; port = 8017 }
    "18" = @{ name = "cart-service"; port = 8018 }
    "19" = @{ name = "search-service"; port = 8019 }
    "20" = @{ name = "recommendation-service"; port = 8020 }
    "21" = @{ name = "review-service"; port = 8021 }
    "22" = @{ name = "wishlist-service"; port = 8022 }
    "23" = @{ name = "analytics-service"; port = 8023 }
    "24" = @{ name = "reporting-service"; port = 8024 }
    "25" = @{ name = "inventory-service"; port = 8025 }
    "26" = @{ name = "shipping-service"; port = 8026 }
    "27" = @{ name = "invoice-service"; port = 8027 }
    "28" = @{ name = "chat-service"; port = 8028 }
    "29" = @{ name = "video-call-service"; port = 8029 }
    "30" = @{ name = "geolocation-service"; port = 8030 }
    "31" = @{ name = "subscription-service"; port = 8031 }
    "32" = @{ name = "loyalty-service"; port = 8032 }
    "33" = @{ name = "coupon-service"; port = 8033 }
    "34" = @{ name = "referral-service"; port = 8034 }
    "35" = @{ name = "translation-service"; port = 8035 }
    "36" = @{ name = "cms-service"; port = 8036 }
    "37" = @{ name = "feedback-service"; port = 8037 }
    "38" = @{ name = "monitoring-service"; port = 8038 }
    "39" = @{ name = "logging-service"; port = 8039 }
    "40" = @{ name = "scheduler-service"; port = 8040 }
    "41" = @{ name = "webhook-service"; port = 8041 }
    "42" = @{ name = "export-service"; port = 8042 }
    "43" = @{ name = "import-service"; port = 8043 }
    "44" = @{ name = "backup-service"; port = 8044 }
    "45" = @{ name = "rate-limiter-service"; port = 8045 }
    "46" = @{ name = "ab-testing-service"; port = 8046 }
    "47" = @{ name = "feature-flag-service"; port = 8047 }
    "48" = @{ name = "tax-service"; port = 8048 }
    "49" = @{ name = "fraud-detection-service"; port = 8049 }
    "50" = @{ name = "kyc-service"; port = 8050 }
    "51" = @{ name = "gamification-service"; port = 8051 }
    "52" = @{ name = "social-media-service"; port = 8052 }
}

function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  GitHub Workflows Standardization" -ForegroundColor Cyan
Write-Host "  Range: Service $StartFrom to $EndAt" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  Mode: DRY RUN" -ForegroundColor Yellow
}
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$templatePath = Join-Path $PSScriptRoot "..\gravity-template-service\.github\workflows"
$ciTemplate = Join-Path $templatePath "ci.yml"
$cdTemplate = Join-Path $templatePath "cd.yml"

if (-not (Test-Path $ciTemplate)) {
    Write-Error "CI template not found: $ciTemplate"
    exit 1
}

if (-not (Test-Path $cdTemplate)) {
    Write-Error "CD template not found: $cdTemplate"
    exit 1
}

$updated = 0
$skipped = 0
$errors = 0

foreach ($key in ($services.Keys | Sort-Object)) {
    $number = [int]$key
    
    if ($number -lt $StartFrom -or $number -gt $EndAt) {
        continue
    }

    $serviceInfo = $services[$key]
    $serviceDir = "{0:D2}-{1}" -f $number, $serviceInfo.name
    $servicePath = Join-Path $PSScriptRoot "..\$serviceDir"

    Write-Host "[$number/52] $serviceDir" -ForegroundColor Yellow -NoNewline

    if (-not (Test-Path $servicePath)) {
        Write-Host " - Service directory not found!" -ForegroundColor Red
        $errors++
        continue
    }

    if ($DryRun) {
        Write-Host " - Would update workflows" -ForegroundColor Cyan
        $updated++
        continue
    }

    try {
        # Create .github/workflows directory
        $workflowsPath = Join-Path $servicePath ".github\workflows"
        if (-not (Test-Path $workflowsPath)) {
            New-Item -ItemType Directory -Path $workflowsPath -Force | Out-Null
        }

        # Read templates
        $ciContent = Get-Content $ciTemplate -Raw
        $cdContent = Get-Content $cdTemplate -Raw

        # Replace placeholders
        $ciContent = $ciContent -replace 'template-service', $serviceInfo.name
        $ciContent = $ciContent -replace 'Template Service', ($serviceInfo.name -replace '-', ' ' | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) })
        
        $cdContent = $cdContent -replace 'template-service', $serviceInfo.name
        $cdContent = $cdContent -replace 'Template Service', ($serviceInfo.name -replace '-', ' ' | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) })

        # Write files
        $ciPath = Join-Path $workflowsPath "ci.yml"
        $cdPath = Join-Path $workflowsPath "cd.yml"

        $ciContent | Out-File -FilePath $ciPath -Encoding UTF8 -NoNewline
        $cdContent | Out-File -FilePath $cdPath -Encoding UTF8 -NoNewline

        Write-Host " ✅ Updated" -ForegroundColor Green
        $updated++
    }
    catch {
        Write-Host " ❌ Error: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Updated: $updated" -ForegroundColor Green
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "  Errors:  $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })
Write-Host "================================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host ""
    Write-Warning "This was a DRY RUN. No changes were made."
    Write-Info "Run without -DryRun to perform actual updates."
}
