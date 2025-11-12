#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Add repository secrets to all service repositories for a given owner.

.DESCRIPTION
    Reads secrets from environment variables or a JSON file and sets them in each repository using `gh secret set`.

.PARAMETER Owner
    GitHub owner (user or org). Default: Shakour-Data

.PARAMETER SecretsFile
    Optional path to a JSON file containing secrets. Example:
    {
      "DOCKER_USERNAME": "myuser",
      "DOCKER_PASSWORD": "mypassword",
      "CODECOV_TOKEN": "token"
    }

.PARAMETER DryRun
    If set, the script will only print actions and will not set secrets.

.EXAMPLE
    .\Add-Repo-Secrets.ps1 -Owner Shakour-Data -SecretsFile C:\secrets.json

.NOTES
    Requires GitHub CLI (gh) authenticated.
#>

param(
    [string]$Owner = "Shakour-Data",
    [string]$SecretsFile = "",
    [switch]$DryRun
)

# Services list (same as other scripts)
$services = @(
    "01-common-library",
    "02-service-discovery",
    "03-api-gateway",
    "04-config-service",
    "05-auth-service",
    "06-user-service",
    "07-notification-service",
    "08-email-service",
    "09-sms-service",
    "10-file-storage-service",
    "11-permission-service",
    "12-session-service",
    "13-audit-log-service",
    "14-cache-service",
    "15-payment-service",
    "16-order-service",
    "17-product-service",
    "18-cart-service",
    "19-search-service",
    "20-recommendation-service",
    "21-review-service",
    "22-wishlist-service",
    "23-analytics-service",
    "24-reporting-service",
    "25-inventory-service",
    "26-shipping-service",
    "27-invoice-service",
    "28-chat-service",
    "29-video-call-service",
    "30-geolocation-service",
    "31-subscription-service",
    "32-loyalty-service",
    "33-coupon-service",
    "34-referral-service",
    "35-translation-service",
    "36-cms-service",
    "37-feedback-service",
    "38-monitoring-service",
    "39-logging-service",
    "40-scheduler-service",
    "41-webhook-service",
    "42-export-service",
    "43-import-service",
    "44-backup-service",
    "45-rate-limiter-service",
    "46-ab-testing-service",
    "47-feature-flag-service",
    "48-tax-service",
    "49-fraud-detection-service",
    "50-kyc-service",
    "51-gamification-service",
    "52-social-media-service"
)

function Write-Info { param($m) Write-Host $m -ForegroundColor Cyan }
function Write-Success { param($m) Write-Host $m -ForegroundColor Green }
function Write-Warn { param($m) Write-Host $m -ForegroundColor Yellow }
function Write-Error { param($m) Write-Host $m -ForegroundColor Red }

# Load secrets from file if provided
$secrets = @{}
if ($SecretsFile -ne "" -and (Test-Path $SecretsFile)) {
    try {
        $json = Get-Content $SecretsFile -Raw | ConvertFrom-Json
        foreach ($k in $json.psobject.Properties.Name) { $secrets[$k] = $json.$k }
        Write-Info "Loaded secrets from $SecretsFile"
    }
    catch {
        Write-Error "Failed to load secrets file: $_"
        return
    }
}
else {
    # Read from environment
    $envKeys = @('DOCKER_USERNAME', 'DOCKER_PASSWORD', 'CODECOV_TOKEN')
    foreach ($k in $envKeys) {
        if ($env:$k) { $secrets[$k] = $env:$k }
    }
    if ($secrets.Count -gt 0) { Write-Info "Loaded secrets from environment variables" }
}

if ($secrets.Count -eq 0) {
    Write-Warn "No secrets found. Provide via -SecretsFile or set environment variables. Exiting." 
    return
}

# Confirm which secrets we will set
Write-Host "Secrets to set:" -ForegroundColor Cyan
$secrets.Keys | ForEach-Object { Write-Host "  - $_" }

foreach ($svc in $services) {
    $repo = "$Owner/$svc"
    Write-Host "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "Repository: $repo" -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

    foreach ($key in $secrets.Keys) {
        $value = $secrets[$key]
        if ($DryRun) {
            Write-Info "  [DRY RUN] Would set secret $key on $repo"
            continue
        }

        try {
            Write-Info "  Setting secret $key..."
            gh secret set $key --repo $repo --body "$value" 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) { Write-Success "    ✅ $key set" } else { Write-Error "    ❌ Failed to set $key" }
        }
        catch {
            Write-Error "    ❌ Error setting $key: $_"
        }
    }
}

Write-Host "\nAll done." -ForegroundColor Green
