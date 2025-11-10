<#
.SYNOPSIS
    Clone all Gravity microservice repositories

.DESCRIPTION
    Clones all 52 Gravity microservice repositories from GitHub to a local directory

.PARAMETER TargetDirectory
    Directory where repositories will be cloned (default: current directory)

.PARAMETER GitHubOrg
    GitHub organization name (default: "GravityMicroServices")

.PARAMETER Parallel
    Number of parallel clones (default: 5)

.EXAMPLE
    .\Clone-AllRepositories.ps1 -TargetDirectory "C:\Projects\Gravity"

.NOTES
    Author: Gravity Elite Engineering Team
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory = $false)]
    [string]$TargetDirectory = ".",

    [Parameter(Mandatory = $false)]
    [string]$GitHubOrg = "GravityMicroServices",

    [Parameter(Mandatory = $false)]
    [ValidateRange(1, 10)]
    [int]$Parallel = 5
)

$ErrorActionPreference = "Continue"

function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }

# Service names
$ServiceNames = @(
    "common-library", "service-discovery", "api-gateway", "config-server",
    "auth-service", "user-service", "notification-service", "email-service",
    "sms-service", "push-notification-service", "payment-service", "order-service",
    "product-service", "inventory-service", "shipping-service", "tracking-service",
    "analytics-service", "reporting-service", "logging-service", "monitoring-service",
    "search-service", "recommendation-service", "review-service", "rating-service",
    "cart-service", "wishlist-service", "coupon-service", "loyalty-service",
    "refund-service", "invoice-service", "tax-service", "pricing-service",
    "catalog-service", "media-service", "content-service", "cms-service",
    "localization-service", "translation-service", "file-storage-service", "backup-service",
    "scheduler-service", "webhook-service", "audit-service", "compliance-service",
    "gdpr-service", "chat-service", "video-call-service", "geolocation-service",
    "map-service", "weather-service", "ai-ml-service", "social-media-service"
)

Write-Info "Cloning all Gravity repositories to: $TargetDirectory"
Write-Info "Total repositories: $($ServiceNames.Count)"

# Create target directory
New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null

# Clone repositories
$Counter = 0
foreach ($serviceName in $ServiceNames) {
    $Counter++
    $RepoName = "gravity-$serviceName"
    $RepoUrl = "https://github.com/$GitHubOrg/$RepoName.git"
    $LocalPath = Join-Path $TargetDirectory $RepoName
    
    Write-Info "[$Counter/$($ServiceNames.Count)] Cloning $RepoName..."
    
    if (Test-Path $LocalPath) {
        Write-Warning "Already exists: $LocalPath"
    }
    else {
        git clone $RepoUrl $LocalPath
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Cloned: $RepoName"
        }
        else {
            Write-Host "Failed to clone: $RepoName" -ForegroundColor Red
        }
    }
}

Write-Success "Cloning completed!"
