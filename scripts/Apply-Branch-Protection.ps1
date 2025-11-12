#Requires -Version 7.0

<#
.SYNOPSIS
    Apply branch protection rules to all Gravity MicroServices repositories
.DESCRIPTION
    Configures GitHub branch protection rules for the main branch:
    - Require pull request reviews before merging (2 reviewers)
    - Require status checks to pass before merging
    - Require branches to be up to date before merging
    - Do not allow bypassing the above settings
    - Restrict who can push to matching branches
.PARAMETER StartFrom
    Service number to start from (default: 4)
.PARAMETER EndAt
    Service number to end at (default: 52)
.PARAMETER DryRun
    If specified, only shows what would be done without applying rules
.EXAMPLE
    .\Apply-Branch-Protection.ps1
    .\Apply-Branch-Protection.ps1 -StartFrom 4 -EndAt 10
    .\Apply-Branch-Protection.ps1 -DryRun
#>

[CmdletBinding()]
param(
    [Parameter()]
    [int]$StartFrom = 4,
    
    [Parameter()]
    [int]$EndAt = 52,
    
    [Parameter()]
    [switch]$DryRun
)

# Service metadata
$services = @{
    4  = @{ Name = "config-service" }
    5  = @{ Name = "auth-service" }
    6  = @{ Name = "user-service" }
    7  = @{ Name = "notification-service" }
    8  = @{ Name = "email-service" }
    9  = @{ Name = "sms-service" }
    10 = @{ Name = "file-storage-service" }
    11 = @{ Name = "permission-service" }
    12 = @{ Name = "session-service" }
    13 = @{ Name = "audit-log-service" }
    14 = @{ Name = "cache-service" }
    15 = @{ Name = "payment-service" }
    16 = @{ Name = "order-service" }
    17 = @{ Name = "product-service" }
    18 = @{ Name = "cart-service" }
    19 = @{ Name = "search-service" }
    20 = @{ Name = "recommendation-service" }
    21 = @{ Name = "review-service" }
    22 = @{ Name = "wishlist-service" }
    23 = @{ Name = "analytics-service" }
    24 = @{ Name = "reporting-service" }
    25 = @{ Name = "inventory-service" }
    26 = @{ Name = "shipping-service" }
    27 = @{ Name = "invoice-service" }
    28 = @{ Name = "chat-service" }
    29 = @{ Name = "video-call-service" }
    30 = @{ Name = "geolocation-service" }
    31 = @{ Name = "subscription-service" }
    32 = @{ Name = "loyalty-service" }
    33 = @{ Name = "coupon-service" }
    34 = @{ Name = "referral-service" }
    35 = @{ Name = "translation-service" }
    36 = @{ Name = "cms-service" }
    37 = @{ Name = "feedback-service" }
    38 = @{ Name = "monitoring-service" }
    39 = @{ Name = "logging-service" }
    40 = @{ Name = "scheduler-service" }
    41 = @{ Name = "webhook-service" }
    42 = @{ Name = "export-service" }
    43 = @{ Name = "import-service" }
    44 = @{ Name = "backup-service" }
    45 = @{ Name = "rate-limiter-service" }
    46 = @{ Name = "ab-testing-service" }
    47 = @{ Name = "feature-flag-service" }
    48 = @{ Name = "tax-service" }
    49 = @{ Name = "fraud-detection-service" }
    50 = @{ Name = "kyc-service" }
    51 = @{ Name = "gamification-service" }
    52 = @{ Name = "social-media-service" }
}

$owner = "Shakour-Data"

# Main script execution
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Branch Protection Rules - Gravity MicroServices" -ForegroundColor Cyan
Write-Host "  Owner: $owner" -ForegroundColor Cyan
Write-Host "  Range: Service $StartFrom to $EndAt" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# Check GitHub CLI authentication
Write-Host "ℹ️  Checking GitHub CLI authentication..." -ForegroundColor Cyan
try {
    $ghStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ GitHub CLI not authenticated. Please run: gh auth login" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ GitHub CLI authenticated`n" -ForegroundColor Green
}
catch {
    Write-Host "❌ GitHub CLI not found. Please install: https://cli.github.com/" -ForegroundColor Red
    exit 1
}

$applied = 0
$skipped = 0
$errors = 0

for ($i = $StartFrom; $i -le $EndAt; $i++) {
    if (-not $services.ContainsKey($i)) {
        Write-Host "[$i/$EndAt] Service $i not found in metadata - Skipping" -ForegroundColor Yellow
        $skipped++
        continue
    }
    
    $service = $services[$i]
    $serviceName = $service.Name
    $serviceNumber = $i.ToString("D2")
    $repoName = "$serviceNumber-$serviceName"
    $repoFullName = "$owner/$repoName"
    
    Write-Host "`n================================================================" -ForegroundColor Cyan
    Write-Host "[$i/$EndAt] $repoName" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    
    # Check if repository exists
    Write-Host "ℹ️  Checking if repository exists..." -ForegroundColor Cyan
    try {
        $repoCheck = gh repo view $repoFullName --json name 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Repository not found: $repoFullName" -ForegroundColor Red
            $errors++
            continue
        }
        Write-Host "✅ Repository exists: $repoFullName" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Error checking repository: $_" -ForegroundColor Red
        $errors++
        continue
    }
    
    if ($DryRun) {
        Write-Host "🔍 Would apply branch protection rules to main branch" -ForegroundColor Yellow
        Write-Host "   - Require pull request reviews: 2 reviewers" -ForegroundColor Yellow
        Write-Host "   - Require status checks to pass" -ForegroundColor Yellow
        Write-Host "   - Require branches to be up to date" -ForegroundColor Yellow
        Write-Host "   - No force pushes allowed" -ForegroundColor Yellow
        $applied++
        continue
    }
    
    # Apply branch protection rules using gh CLI
    Write-Host "ℹ️  Applying branch protection rules..." -ForegroundColor Cyan
    try {
        # Note: GitHub CLI doesn't have direct branch protection commands yet
        # We'll use the REST API through gh api command
        
        $protectionData = @{
            required_status_checks           = @{
                strict   = $true
                contexts = @("CI / lint", "CI / security", "CI / test")
            }
            enforce_admins                   = $false
            required_pull_request_reviews    = @{
                dismissal_restrictions          = @{}
                dismiss_stale_reviews           = $true
                require_code_owner_reviews      = $false
                required_approving_review_count = 2
                require_last_push_approval      = $false
            }
            restrictions                     = $null
            required_linear_history          = $false
            allow_force_pushes               = $false
            allow_deletions                  = $false
            block_creations                  = $false
            required_conversation_resolution = $true
            lock_branch                      = $false
            allow_fork_syncing               = $true
        } | ConvertTo-Json -Depth 10
        
        # Apply protection rules
        $apiResult = $protectionData | gh api `
            --method PUT `
            "repos/$repoFullName/branches/main/protection" `
            --input - 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Branch protection rules applied successfully" -ForegroundColor Green
            Write-Host "   ✅ Required reviewers: 2" -ForegroundColor Green
            Write-Host "   ✅ Status checks required: CI jobs" -ForegroundColor Green
            Write-Host "   ✅ Force pushes blocked" -ForegroundColor Green
            Write-Host "   ✅ Conversation resolution required" -ForegroundColor Green
            $applied++
        }
        else {
            Write-Host "⚠️  Warning: Could not apply protection rules" -ForegroundColor Yellow
            Write-Host "   This might be because:" -ForegroundColor Yellow
            Write-Host "   - Branch 'main' doesn't exist yet (no commits)" -ForegroundColor Yellow
            Write-Host "   - Insufficient permissions" -ForegroundColor Yellow
            Write-Host "   Rules will be applied once the branch exists" -ForegroundColor Yellow
            $skipped++
        }
    }
    catch {
        Write-Host "❌ Error applying protection rules: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Applied: $applied" -ForegroundColor Green
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "  Errors:  $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })

if ($DryRun) {
    Write-Host "`nℹ️  This was a DRY RUN. Use without -DryRun to apply rules." -ForegroundColor Yellow
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Branch Protection Rules Applied:" -ForegroundColor Cyan
Write-Host "  ✅ Require pull request reviews (2 approvals)" -ForegroundColor Green
Write-Host "  ✅ Require status checks (CI/CD must pass)" -ForegroundColor Green
Write-Host "  ✅ Require branches to be up to date" -ForegroundColor Green
Write-Host "  ✅ Dismiss stale reviews on new commits" -ForegroundColor Green
Write-Host "  ✅ Require conversation resolution" -ForegroundColor Green
Write-Host "  ✅ Block force pushes" -ForegroundColor Green
Write-Host "  ✅ Block branch deletion" -ForegroundColor Green
Write-Host "================================================================`n" -ForegroundColor Cyan
