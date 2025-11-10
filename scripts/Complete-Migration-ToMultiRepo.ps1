# ================================================================================
# Gravity MicroServices - Complete Migration to Multi-Repo
# ================================================================================
# This script orchestrates the full migration of all 52 services from monorepo
# to separate GitHub repositories with complete Git history preservation
#
# Author: DevOps Team
# Date: November 10, 2025
# ================================================================================

param(
    [string]$OrgName = "GravityMicroservices",
    [string]$MonorepoPath = "E:\Shakour\GravityMicroServices",
    [string]$TempPath = "E:\Shakour\GravityMicroServices_Migration",
    [ValidateSet("public", "private")]
    [string]$Visibility = "public",
    [switch]$DryRun = $false,
    [switch]$CreateOrg = $true,
    [switch]$SkipBackup = $false
)

# ================================================================================
# Configuration
# ================================================================================

$ErrorActionPreference = "Stop"
$ProgressPreference = "Continue"

# All 52 services to migrate
$services = @(
    @{Number = 1; Path = "01-common-library"; Name = "common-library"; Priority = "P0" },
    @{Number = 2; Path = "02-service-discovery"; Name = "service-discovery"; Priority = "P0" },
    @{Number = 3; Path = "03-api-gateway"; Name = "api-gateway"; Priority = "P0" },
    @{Number = 4; Path = "04-config-service"; Name = "config-service"; Priority = "P0" },
    @{Number = 5; Path = "05-auth-service"; Name = "auth-service"; Priority = "P1" },
    @{Number = 6; Path = "06-user-service"; Name = "user-service"; Priority = "P1" },
    @{Number = 7; Path = "07-notification-service"; Name = "notification-service"; Priority = "P1" },
    @{Number = 8; Path = "08-email-service"; Name = "email-service"; Priority = "P1" },
    @{Number = 9; Path = "09-sms-service"; Name = "sms-service"; Priority = "P1" },
    @{Number = 10; Path = "10-file-storage-service"; Name = "file-storage-service"; Priority = "P1" },
    @{Number = 11; Path = "11-permission-service"; Name = "permission-service"; Priority = "P1" },
    @{Number = 12; Path = "12-session-service"; Name = "session-service"; Priority = "P1" },
    @{Number = 13; Path = "13-audit-log-service"; Name = "audit-log-service"; Priority = "P1" },
    @{Number = 14; Path = "14-cache-service"; Name = "cache-service"; Priority = "P1" },
    @{Number = 15; Path = "15-payment-service"; Name = "payment-service"; Priority = "P2" },
    @{Number = 16; Path = "16-order-service"; Name = "order-service"; Priority = "P2" },
    @{Number = 17; Path = "17-product-service"; Name = "product-service"; Priority = "P2" },
    @{Number = 18; Path = "18-cart-service"; Name = "cart-service"; Priority = "P2" },
    @{Number = 19; Path = "19-search-service"; Name = "search-service"; Priority = "P2" },
    @{Number = 20; Path = "20-recommendation-service"; Name = "recommendation-service"; Priority = "P2" },
    @{Number = 21; Path = "21-review-service"; Name = "review-service"; Priority = "P2" },
    @{Number = 22; Path = "22-wishlist-service"; Name = "wishlist-service"; Priority = "P2" },
    @{Number = 23; Path = "23-analytics-service"; Name = "analytics-service"; Priority = "P2" },
    @{Number = 24; Path = "24-reporting-service"; Name = "reporting-service"; Priority = "P2" },
    @{Number = 25; Path = "25-inventory-service"; Name = "inventory-service"; Priority = "P2" },
    @{Number = 26; Path = "26-shipping-service"; Name = "shipping-service"; Priority = "P2" },
    @{Number = 27; Path = "27-invoice-service"; Name = "invoice-service"; Priority = "P2" },
    @{Number = 28; Path = "28-chat-service"; Name = "chat-service"; Priority = "P3" },
    @{Number = 29; Path = "29-video-call-service"; Name = "video-call-service"; Priority = "P3" },
    @{Number = 30; Path = "30-geolocation-service"; Name = "geolocation-service"; Priority = "P3" },
    @{Number = 31; Path = "31-subscription-service"; Name = "subscription-service"; Priority = "P3" },
    @{Number = 32; Path = "32-loyalty-service"; Name = "loyalty-service"; Priority = "P3" },
    @{Number = 33; Path = "33-coupon-service"; Name = "coupon-service"; Priority = "P3" },
    @{Number = 34; Path = "34-referral-service"; Name = "referral-service"; Priority = "P3" },
    @{Number = 35; Path = "35-translation-service"; Name = "translation-service"; Priority = "P3" },
    @{Number = 36; Path = "36-cms-service"; Name = "cms-service"; Priority = "P3" },
    @{Number = 37; Path = "37-feedback-service"; Name = "feedback-service"; Priority = "P3" },
    @{Number = 38; Path = "38-monitoring-service"; Name = "monitoring-service"; Priority = "P4" },
    @{Number = 39; Path = "39-logging-service"; Name = "logging-service"; Priority = "P4" },
    @{Number = 40; Path = "40-scheduler-service"; Name = "scheduler-service"; Priority = "P4" },
    @{Number = 41; Path = "41-webhook-service"; Name = "webhook-service"; Priority = "P4" },
    @{Number = 42; Path = "42-export-service"; Name = "export-service"; Priority = "P4" },
    @{Number = 43; Path = "43-import-service"; Name = "import-service"; Priority = "P4" },
    @{Number = 44; Path = "44-backup-service"; Name = "backup-service"; Priority = "P4" },
    @{Number = 45; Path = "45-rate-limiter-service"; Name = "rate-limiter-service"; Priority = "P4" },
    @{Number = 46; Path = "46-ab-testing-service"; Name = "ab-testing-service"; Priority = "P4" },
    @{Number = 47; Path = "47-feature-flag-service"; Name = "feature-flag-service"; Priority = "P4" },
    @{Number = 48; Path = "48-tax-service"; Name = "tax-service"; Priority = "P4" },
    @{Number = 49; Path = "49-fraud-detection-service"; Name = "fraud-detection-service"; Priority = "P4" },
    @{Number = 50; Path = "50-kyc-service"; Name = "kyc-service"; Priority = "P4" },
    @{Number = 51; Path = "51-gamification-service"; Name = "gamification-service"; Priority = "P4" },
    @{Number = 52; Path = "52-social-media-service"; Name = "social-media-service"; Priority = "P4" }
)

# ================================================================================
# Functions
# ================================================================================

function Write-Banner {
    param([string]$Message)
    Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  $Message" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
}

function Write-Step {
    param([string]$Message)
    Write-Host "`n▶ $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Test-Prerequisites {
    Write-Step "Checking prerequisites..."
    
    # Check Git
    try {
        $gitVersion = git --version
        Write-Success "Git installed: $gitVersion"
    }
    catch {
        Write-Error "Git is not installed!"
        return $false
    }
    
    # Check GitHub CLI
    try {
        $ghVersion = gh --version 2>&1 | Select-Object -First 1
        Write-Success "GitHub CLI installed: $ghVersion"
    }
    catch {
        Write-Error "GitHub CLI (gh) is not installed!"
        Write-Info "Install from: https://cli.github.com/"
        return $false
    }
    
    # Check authentication
    try {
        $authStatus = gh auth status 2>&1
        if ($authStatus -match "Logged in") {
            Write-Success "GitHub CLI authenticated"
        }
        else {
            Write-Error "GitHub CLI not authenticated!"
            Write-Info "Run: gh auth login"
            return $false
        }
    }
    catch {
        Write-Error "GitHub CLI authentication failed!"
        return $false
    }
    
    # Check monorepo exists
    if (-not (Test-Path $MonorepoPath)) {
        Write-Error "Monorepo not found at: $MonorepoPath"
        return $false
    }
    Write-Success "Monorepo found: $MonorepoPath"
    
    return $true
}

function New-GitHubOrganization {
    Write-Step "Creating GitHub Organization: $OrgName"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create organization: $OrgName"
        return $true
    }
    
    # Check if organization exists
    try {
        gh api "/orgs/$OrgName" 2>&1 | Out-Null
        Write-Info "Organization '$OrgName' already exists"
        return $true
    }
    catch {
        Write-Info "Organization does not exist, attempting to create..."
    }
    
    Write-Info "Please create the organization manually:"
    Write-Host "   1. Go to: https://github.com/organizations/new" -ForegroundColor White
    Write-Host "   2. Name: $OrgName" -ForegroundColor White
    Write-Host "   3. Plan: Free (or your choice)" -ForegroundColor White
    Write-Host "   4. Press Enter when done..." -ForegroundColor Yellow
    Read-Host
    
    # Verify creation
    try {
        gh api "/orgs/$OrgName" 2>&1 | Out-Null
        Write-Success "Organization '$OrgName' verified!"
        return $true
    }
    catch {
        Write-Error "Organization verification failed!"
        return $false
    }
}

function Backup-Monorepo {
    if ($SkipBackup) {
        Write-Info "Backup skipped (as requested)"
        return $true
    }
    
    Write-Step "Creating backup of monorepo..."
    
    $backupPath = "$MonorepoPath`_BACKUP_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    
    try {
        if ($DryRun) {
            Write-Info "[DRY RUN] Would backup to: $backupPath"
        }
        else {
            Copy-Item -Path $MonorepoPath -Destination $backupPath -Recurse -Force
            Write-Success "Backup created: $backupPath"
        }
        return $true
    }
    catch {
        Write-Error "Backup failed: $_"
        return $false
    }
}

function Split-ServiceWithHistory {
    param(
        [hashtable]$Service
    )
    
    Write-Step "Splitting service: $($Service.Name) ($($Service.Priority))"
    
    $servicePath = $Service.Path
    $serviceName = $Service.Name
    $tempBranch = "split-$serviceName"
    
    Push-Location $MonorepoPath
    
    try {
        # Create split branch with service history
        Write-Info "Extracting Git history for $servicePath..."
        if ($DryRun) {
            Write-Info "[DRY RUN] Would run: git subtree split --prefix=$servicePath --branch=$tempBranch"
        }
        else {
            git subtree split --prefix=$servicePath --branch=$tempBranch 2>&1 | Out-Null
            Write-Success "History extracted to branch: $tempBranch"
        }
        
        return $tempBranch
    }
    catch {
        Write-Error "Failed to split service: $_"
        return $null
    }
    finally {
        Pop-Location
    }
}

function New-ServiceRepository {
    param(
        [hashtable]$Service,
        [string]$BranchName
    )
    
    $serviceName = $Service.Name
    $serviceNumber = $Service.Number
    $repoName = "{0:D2}-$serviceName" -f $serviceNumber
    
    Write-Step "Creating repository: $OrgName/$repoName"
    
    $tempRepoPath = Join-Path $TempPath $repoName
    
    try {
        # Create temp directory
        if (Test-Path $tempRepoPath) {
            Remove-Item $tempRepoPath -Recurse -Force
        }
        New-Item -ItemType Directory -Path $tempRepoPath -Force | Out-Null
        
        # Initialize new repo with extracted history
        Push-Location $tempRepoPath
        
        if ($DryRun) {
            Write-Info "[DRY RUN] Would initialize repo and push to: $OrgName/$repoName"
        }
        else {
            git init | Out-Null
            git pull "$MonorepoPath/.git" $BranchName | Out-Null
            
            # Create repository on GitHub
            Write-Info "Creating GitHub repository..."
            gh repo create "$OrgName/$repoName" --public --description "Gravity MicroServices - $serviceName" 2>&1 | Out-Null
            
            # Push to GitHub
            git remote add origin "https://github.com/$OrgName/$repoName.git"
            git branch -M main
            git push -u origin main
            
            Write-Success "Repository created and pushed: $OrgName/$repoName"
        }
        
        Pop-Location
        return $true
    }
    catch {
        Write-Error "Failed to create repository: $_"
        if ((Get-Location).Path -ne $PSScriptRoot) {
            Pop-Location
        }
        return $false
    }
}

function Remove-TempBranch {
    param([string]$BranchName)
    
    Push-Location $MonorepoPath
    try {
        if ($DryRun) {
            Write-Info "[DRY RUN] Would delete branch: $BranchName"
        }
        else {
            git branch -D $BranchName 2>&1 | Out-Null
        }
    }
    catch {
        Write-Info "Could not delete branch $BranchName (may not exist)"
    }
    finally {
        Pop-Location
    }
}

# ================================================================================
# Main Execution
# ================================================================================

function Start-Migration {
    Write-Banner "🚀 GRAVITY MICROSERVICES - FULL MIGRATION TO MULTI-REPO"
    
    Write-Host "`nConfiguration:" -ForegroundColor Cyan
    Write-Host "  Organization: $OrgName" -ForegroundColor White
    Write-Host "  Monorepo: $MonorepoPath" -ForegroundColor White
    Write-Host "  Temp Path: $TempPath" -ForegroundColor White
    Write-Host "  Services: $($services.Count)" -ForegroundColor White
    Write-Host "  Dry Run: $DryRun" -ForegroundColor White
    
    if (-not $DryRun) {
        Write-Host "`n⚠️  WARNING: This will create 52 new repositories!" -ForegroundColor Yellow
        Write-Host "Are you sure you want to continue? (Y/N): " -ForegroundColor Yellow -NoNewline
        $confirm = Read-Host
        if ($confirm -ne "Y" -and $confirm -ne "y") {
            Write-Info "Migration cancelled"
            return
        }
    }
    
    # Step 1: Prerequisites
    Write-Banner "STEP 1: Prerequisites Check"
    if (-not (Test-Prerequisites)) {
        Write-Error "Prerequisites check failed!"
        return
    }
    
    # Step 2: Create Organization
    if ($CreateOrg) {
        Write-Banner "STEP 2: GitHub Organization Setup"
        if (-not (New-GitHubOrganization)) {
            Write-Error "Organization setup failed!"
            return
        }
    }
    
    # Step 3: Backup
    Write-Banner "STEP 3: Monorepo Backup"
    if (-not (Backup-Monorepo)) {
        Write-Error "Backup failed!"
        return
    }
    
    # Step 4: Create temp directory
    Write-Banner "STEP 4: Preparation"
    if (-not $DryRun) {
        if (Test-Path $TempPath) {
            Write-Info "Cleaning temp directory..."
            Remove-Item $TempPath -Recurse -Force
        }
        New-Item -ItemType Directory -Path $TempPath -Force | Out-Null
        Write-Success "Temp directory created: $TempPath"
    }
    
    # Step 5: Migrate each service
    Write-Banner "STEP 5: Migrating All 52 Services"
    
    $successCount = 0
    $failedServices = @()
    
    foreach ($service in $services) {
        Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host "Service $($service.Number)/52: $($service.Name)" -ForegroundColor Cyan
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        
        try {
            # Split service
            $branchName = Split-ServiceWithHistory -Service $service
            if (-not $branchName) {
                throw "Failed to split service"
            }
            
            # Create repository
            if (-not (New-ServiceRepository -Service $service -BranchName $branchName)) {
                throw "Failed to create repository"
            }
            
            # Cleanup
            Remove-TempBranch -BranchName $branchName
            
            $successCount++
            Write-Success "Service $($service.Name) migrated successfully! ($successCount/52)"
            
            # Small delay to avoid rate limiting
            if (-not $DryRun) {
                Start-Sleep -Seconds 2
            }
        }
        catch {
            Write-Error "Failed to migrate $($service.Name): $_"
            $failedServices += $service
        }
    }
    
    # Final Report
    Write-Banner "MIGRATION COMPLETE"
    
    Write-Host "`nResults:" -ForegroundColor Cyan
    Write-Host "  ✅ Successful: $successCount/52" -ForegroundColor Green
    Write-Host "  ❌ Failed: $($failedServices.Count)/52" -ForegroundColor $(if ($failedServices.Count -gt 0) { "Red" } else { "Green" })
    
    if ($failedServices.Count -gt 0) {
        Write-Host "`nFailed Services:" -ForegroundColor Red
        foreach ($service in $failedServices) {
            Write-Host "  - $($service.Name)" -ForegroundColor Yellow
        }
    }
    
    if ($successCount -eq 52) {
        Write-Host "`n🎉 ALL 52 SERVICES MIGRATED SUCCESSFULLY! 🎉" -ForegroundColor Green
        Write-Host "`nNext Steps:" -ForegroundColor Cyan
        Write-Host "  1. Configure branch protection for each repo" -ForegroundColor White
        Write-Host "  2. Set up CI/CD workflows" -ForegroundColor White
        Write-Host "  3. Update team permissions" -ForegroundColor White
        Write-Host "  4. Update documentation" -ForegroundColor White
        Write-Host "  5. Archive monorepo" -ForegroundColor White
        Write-Host "`nOrganization: https://github.com/$OrgName" -ForegroundColor Cyan
    }
}

# Execute migration
Start-Migration
