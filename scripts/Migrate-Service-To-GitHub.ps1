# ============================================================================
# Script: Migrate-Service-To-GitHub.ps1
# Purpose: Push individual services from Monorepo to GitHub repositories
# Author: Gravity Elite Team
# Date: 2024
# ============================================================================

param(
    [Parameter(Mandatory = $false)]
    [int]$ServiceNumber,
    
    [Parameter(Mandatory = $false)]
    [int]$StartFrom = 4,
    
    [Parameter(Mandatory = $false)]
    [int]$EndAt = 52,
    
    [Parameter(Mandatory = $false)]
    [string]$GitHubOwner = "Shakour-Data",
    
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Service metadata
$services = @{
    "04" = @{ name = "config-service"; desc = "Configuration Management Service" }
    "05" = @{ name = "auth-service"; desc = "Authentication & Authorization Service" }
    "06" = @{ name = "user-service"; desc = "User Profile & Management Service" }
    "07" = @{ name = "notification-service"; desc = "Multi-Channel Notification Service" }
    "08" = @{ name = "email-service"; desc = "Email Delivery Service" }
    "09" = @{ name = "sms-service"; desc = "SMS Delivery Service" }
    "10" = @{ name = "file-storage-service"; desc = "File Storage & Management Service" }
    "11" = @{ name = "permission-service"; desc = "RBAC Permissions Service" }
    "12" = @{ name = "session-service"; desc = "User Session Management Service" }
    "13" = @{ name = "audit-log-service"; desc = "Audit & Activity Logging Service" }
    "14" = @{ name = "cache-service"; desc = "Distributed Cache Service" }
    "15" = @{ name = "payment-service"; desc = "Payment Processing Service" }
    "16" = @{ name = "order-service"; desc = "Order Management Service" }
    "17" = @{ name = "product-service"; desc = "Product Catalog Service" }
    "18" = @{ name = "cart-service"; desc = "Shopping Cart Service" }
    "19" = @{ name = "search-service"; desc = "Search & Indexing Service" }
    "20" = @{ name = "recommendation-service"; desc = "AI Recommendation Engine" }
    "21" = @{ name = "review-service"; desc = "Product Review & Rating Service" }
    "22" = @{ name = "wishlist-service"; desc = "Wishlist Management Service" }
    "23" = @{ name = "analytics-service"; desc = "Analytics & Metrics Service" }
    "24" = @{ name = "reporting-service"; desc = "Report Generation Service" }
    "25" = @{ name = "inventory-service"; desc = "Inventory Management Service" }
    "26" = @{ name = "shipping-service"; desc = "Shipping & Logistics Service" }
    "27" = @{ name = "invoice-service"; desc = "Invoice Generation Service" }
    "28" = @{ name = "chat-service"; desc = "Real-time Chat Service" }
    "29" = @{ name = "video-call-service"; desc = "Video Call Service" }
    "30" = @{ name = "geolocation-service"; desc = "Geolocation Service" }
    "31" = @{ name = "subscription-service"; desc = "Subscription Management Service" }
    "32" = @{ name = "loyalty-service"; desc = "Loyalty Program Service" }
    "33" = @{ name = "coupon-service"; desc = "Coupon & Discount Service" }
    "34" = @{ name = "referral-service"; desc = "Referral Program Service" }
    "35" = @{ name = "translation-service"; desc = "i18n Translation Service" }
    "36" = @{ name = "cms-service"; desc = "Content Management Service" }
    "37" = @{ name = "feedback-service"; desc = "Feedback & Survey Service" }
    "38" = @{ name = "monitoring-service"; desc = "System Monitoring Service" }
    "39" = @{ name = "logging-service"; desc = "Centralized Logging Service" }
    "40" = @{ name = "scheduler-service"; desc = "Task Scheduler Service" }
    "41" = @{ name = "webhook-service"; desc = "Webhook Management Service" }
    "42" = @{ name = "export-service"; desc = "Data Export Service" }
    "43" = @{ name = "import-service"; desc = "Data Import Service" }
    "44" = @{ name = "backup-service"; desc = "Backup & Restore Service" }
    "45" = @{ name = "rate-limiter-service"; desc = "Rate Limiting Service" }
    "46" = @{ name = "ab-testing-service"; desc = "A/B Testing Service" }
    "47" = @{ name = "feature-flag-service"; desc = "Feature Flag Service" }
    "48" = @{ name = "tax-service"; desc = "Tax Calculation Service" }
    "49" = @{ name = "fraud-detection-service"; desc = "Fraud Detection Service" }
    "50" = @{ name = "kyc-service"; desc = "KYC Verification Service" }
    "51" = @{ name = "gamification-service"; desc = "Gamification Service" }
    "52" = @{ name = "social-media-service"; desc = "Social Media Integration Service" }
}

function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }

function Push-ServiceToGitHub {
    param(
        [string]$ServiceNumber,
        [hashtable]$ServiceInfo,
        [string]$Owner,
        [bool]$IsDryRun
    )
    
    $serviceDir = "{0:D2}-{1}" -f [int]$ServiceNumber, $ServiceInfo.name
    $repoName = $serviceDir  # Use serviceDir instead (includes number)
    $repoUrl = "https://github.com/$Owner/$repoName.git"
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "[$ServiceNumber/52] $serviceDir" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor Cyan
    
    # Check if service directory exists
    $servicePath = Join-Path $PSScriptRoot "..\$serviceDir"
    if (-not (Test-Path $servicePath)) {
        Write-Error "Service directory not found: $servicePath"
        return @{ Success = $false; Service = $serviceDir; Error = "Directory not found" }
    }
    
    if ($IsDryRun) {
        Write-Info "DRY RUN: Would migrate $serviceDir to $repoUrl"
        return @{ Success = $true; Service = $serviceDir; DryRun = $true }
    }
    
    try {
        Push-Location $servicePath
        
        # Check if GitHub repo exists
        Write-Info "Checking if repository exists..."
        try {
            gh repo view "$Owner/$repoName" --json name 2>$null | Out-Null
            Write-Success "Repository exists: $Owner/$repoName"
        }
        catch {
            Write-Warning "Repository does not exist: $Owner/$repoName"
            Write-Info "Creating repository..."
            gh repo create "$Owner/$repoName" --public --description $ServiceInfo.desc
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to create repository"
            }
            Write-Success "Repository created successfully"
        }
        
        # Check if .git exists
        if (Test-Path ".git") {
            Write-Info "Git repository already initialized"
            
            # Check current remote
            $currentRemote = git remote get-url origin 2>$null
            if ($currentRemote) {
                Write-Info "Current remote: $currentRemote"
                if ($currentRemote -ne $repoUrl) {
                    Write-Info "Updating remote URL..."
                    git remote set-url origin $repoUrl
                }
            }
            else {
                Write-Info "Adding remote origin..."
                git remote add origin $repoUrl
            }
        }
        else {
            Write-Info "Initializing git repository..."
            git init
            git branch -M main
            git remote add origin $repoUrl
        }
        
        # Check if there are any changes to commit
        $status = git status --porcelain
        if ($status) {
            Write-Info "Staging all files..."
            git add -A
            
            Write-Info "Creating commit..."
            $commitMessage = @"
feat: Initialize $repoName from Monorepo

- Migrated from GravityMicroServices-Archive
- Complete service structure with all configurations
- Docker infrastructure ready
- Environment configuration (.env.example)
- Pydantic Settings config.py
- Poetry dependencies (pyproject.toml)
- Git ignore rules (.gitignore)
- Python 3.12.10 configured

Service: $serviceDir
Description: $($ServiceInfo.desc)
"@
            git commit -m $commitMessage
        }
        else {
            Write-Info "No changes to commit"
        }
        
        # Push to GitHub
        Write-Info "Pushing to GitHub..."
        
        # Fetch to see remote state
        git fetch origin main 2>$null | Out-Null
        
        # Check if remote has commits
        $remoteBranch = git rev-parse origin/main 2>$null
        if ($remoteBranch) {
            Write-Info "Remote has content, pulling first..."
            git pull origin main --allow-unrelated-histories --no-edit -X theirs 2>&1 | Out-Null
        }
        
        # Then push
        $pushResult = git push -u origin main 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Successfully pushed to $repoUrl"
            
            # Verify push
            $remoteCommit = git ls-remote origin main 2>$null | Select-Object -First 1
            if ($remoteCommit) {
                Write-Success "Verified: Code is on GitHub"
            }
            
            return @{ 
                Success = $true
                Service = $serviceDir
                RepoUrl = $repoUrl
                Message = "Migrated successfully"
            }
        }
        else {
            throw "Git push failed: $pushResult"
        }
    }
    catch {
        Write-Error "Failed to migrate $serviceDir : $_"
        return @{ 
            Success = $false
            Service = $serviceDir
            Error   = $_.Exception.Message
        }
    }
    finally {
        Pop-Location
    }
}

# Main execution
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Gravity MicroServices - GitHub Migration" -ForegroundColor Cyan
Write-Host "  Owner: $GitHubOwner" -ForegroundColor Cyan
if ($ServiceNumber) {
    Write-Host "  Service: $ServiceNumber" -ForegroundColor Cyan
}
else {
    Write-Host "  Range: $StartFrom to $EndAt" -ForegroundColor Cyan
}
if ($DryRun) {
    Write-Host "  Mode: DRY RUN" -ForegroundColor Yellow
}
Write-Host "================================================================" -ForegroundColor Cyan

# Check GitHub authentication
Write-Info "Checking GitHub authentication..."
gh auth status 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "GitHub CLI not authenticated. Run: gh auth login"
    exit 1
}
Write-Success "GitHub authentication OK"

$results = @()

if ($ServiceNumber) {
    # Migrate single service
    $serviceKey = "{0:D2}" -f $ServiceNumber
    if ($services.ContainsKey($serviceKey)) {
        $result = Push-ServiceToGitHub -ServiceNumber $serviceKey -ServiceInfo $services[$serviceKey] -Owner $GitHubOwner -IsDryRun $DryRun
        $results += $result
    }
    else {
        Write-Error "Service number $ServiceNumber not found"
        exit 1
    }
}
else {
    # Migrate range of services
    foreach ($key in ($services.Keys | Sort-Object)) {
        $number = [int]$key
        if ($number -ge $StartFrom -and $number -le $EndAt) {
            $result = Push-ServiceToGitHub -ServiceNumber $key -ServiceInfo $services[$key] -Owner $GitHubOwner -IsDryRun $DryRun
            $results += $result
            
            # Small delay to avoid rate limiting
            Start-Sleep -Milliseconds 500
        }
    }
}

# Summary
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Migration Summary" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

$successful = ($results | Where-Object { $_.Success -eq $true }).Count
$failed = ($results | Where-Object { $_.Success -eq $false }).Count

Write-Host "Total: $($results.Count)" -ForegroundColor White
Write-Host "Successful: $successful" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })

if ($failed -gt 0) {
    Write-Host ""
    Write-Host "Failed Services:" -ForegroundColor Red
    $results | Where-Object { $_.Success -eq $false } | ForEach-Object {
        Write-Host "  ❌ $($_.Service): $($_.Error)" -ForegroundColor Red
    }
}

if ($DryRun) {
    Write-Host ""
    Write-Warning "This was a DRY RUN. No changes were made."
    Write-Info "Run without -DryRun to perform actual migration."
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
