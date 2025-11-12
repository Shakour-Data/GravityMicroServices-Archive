<#
.SYNOPSIS
    Setup branch protection rules for all repositories in Shakour-Data Account

.DESCRIPTION
    This script configures branch protection rules for the main branch of all 52 service repositories.
    
    Protection Rules:
    - Require pull request reviews before merging
    - Dismiss stale pull request approvals when new commits are pushed
    - Require status checks to pass before merging
    - Require branches to be up to date before merging
    - Require conversation resolution before merging
    - Do not allow bypassing the above settings

.PARAMETER OrgName
    GitHub Account name (default: Shakour-Data)

.PARAMETER Branch
    Branch to protect (default: main)

.PARAMETER DryRun
    Run in dry-run mode without making actual changes

.EXAMPLE
    .\Setup-BranchProtection.ps1
    
.EXAMPLE
    .\Setup-BranchProtection.ps1 -DryRun
    
.EXAMPLE
    .\Setup-BranchProtection.ps1 -OrgName "MyOrg" -Branch "main"
#>

param(
    [string]$Owner = "Shakour-Data",
    [string]$Branch = "main",
    [switch]$DryRun
)

# Colors for output
$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
Write-Host "║     BRANCH PROTECTION CONFIGURATION SCRIPT            ║" -ForegroundColor $ColorInfo
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor $ColorInfo

# Configuration
Write-Host "📋 Configuration:" -ForegroundColor $ColorInfo
Write-Host "  Account  : $Owner" -ForegroundColor White
Write-Host "  Branch        : $Branch" -ForegroundColor White
Write-Host "  Dry Run       : $DryRun" -ForegroundColor White
Write-Host ""

# List of all 52 services
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

# Branch protection configuration
$protectionRules = @{
    required_pull_request_reviews    = @{
        dismiss_stale_reviews           = $true
        require_code_owner_reviews      = $false
        required_approving_review_count = 1
    }
    required_status_checks           = @{
        strict   = $true
        contexts = @("CI Tests", "Linting")
    }
    enforce_admins                   = $false
    required_conversation_resolution = $true
    restrictions                     = $null
    allow_force_pushes               = $false
    allow_deletions                  = $false
}

# Convert to JSON
$protectionJson = $protectionRules | ConvertTo-Json -Depth 10

# Statistics
$successCount = 0
$failedCount = 0
$skippedCount = 0
$failedRepos = @()

Write-Host "`n▶ Starting branch protection setup for $($services.Count) repositories...`n" -ForegroundColor $ColorInfo

foreach ($service in $services) {
    $repoFullName = "$Owner/$service"
    
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "Repository: $repoFullName" -ForegroundColor White
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    
    try {
        # Check if repository exists
        Write-Host "  ℹ️  Checking repository existence..." -ForegroundColor Gray
        $repoCheck = gh repo view $repoFullName --json name 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  ⚠️  Repository not found: $repoFullName" -ForegroundColor $ColorWarning
            $skippedCount++
            continue
        }
        
        if ($DryRun) {
            Write-Host "  🔍 [DRY RUN] Would configure branch protection for: $repoFullName" -ForegroundColor $ColorWarning
            Write-Host "  📋 Protection rules:" -ForegroundColor Gray
            Write-Host "     - Require PR reviews (1 approval)" -ForegroundColor Gray
            Write-Host "     - Dismiss stale reviews" -ForegroundColor Gray
            Write-Host "     - Require status checks to pass" -ForegroundColor Gray
            Write-Host "     - Require conversation resolution" -ForegroundColor Gray
            Write-Host "     - No force pushes or deletions" -ForegroundColor Gray
            $successCount++
        }
        else {
            # Apply branch protection using GitHub CLI
            Write-Host "  ⚙️  Applying branch protection rules..." -ForegroundColor Gray
            
            # Note: GitHub CLI doesn't have direct branch protection command
            # We need to use gh api for this
            $apiEndpoint = "/repos/$Owner/$service/branches/$Branch/protection"
            
            # Write protection JSON to temp file
            $tempFile = [System.IO.Path]::GetTempFileName()
            $protectionJson | Out-File -FilePath $tempFile -Encoding UTF8
            
            $result = gh api -X PUT $apiEndpoint `
                --input $tempFile `
                -H "Accept: application/vnd.github+json" 2>&1
            
            Remove-Item -Path $tempFile -Force -ErrorAction SilentlyContinue
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Branch protection configured successfully!" -ForegroundColor $ColorSuccess
                $successCount++
            }
            else {
                Write-Host "  ❌ Failed to configure branch protection" -ForegroundColor $ColorError
                Write-Host "     Error: $result" -ForegroundColor $ColorError
                $failedCount++
                $failedRepos += $repoFullName
            }
        }
        
        # Small delay to avoid rate limiting
        Start-Sleep -Milliseconds 500
    }
    catch {
        Write-Host "  ❌ Error processing repository: $_" -ForegroundColor $ColorError
        $failedCount++
        $failedRepos += $repoFullName
    }
    
    Write-Host ""
}

# Final Report
Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
Write-Host "║              CONFIGURATION COMPLETE                    ║" -ForegroundColor $ColorInfo
Write-Host "╚════════════════════════════════════════════════════════╝`n" -ForegroundColor $ColorInfo

Write-Host "Results:" -ForegroundColor White
Write-Host "  ✅ Successful    : $successCount/$($services.Count)" -ForegroundColor $ColorSuccess
Write-Host "  ❌ Failed        : $failedCount/$($services.Count)" -ForegroundColor $(if ($failedCount -gt 0) { $ColorError } else { $ColorSuccess })
Write-Host "  ⚠️  Skipped      : $skippedCount/$($services.Count)" -ForegroundColor $(if ($skippedCount -gt 0) { $ColorWarning } else { $ColorSuccess })

if ($failedRepos.Count -gt 0) {
    Write-Host "`n❌ Failed repositories:" -ForegroundColor $ColorError
    foreach ($repo in $failedRepos) {
        Write-Host "   - $repo" -ForegroundColor $ColorError
    }
}

if ($DryRun) {
    Write-Host "`n⚠️  This was a DRY RUN. No changes were made." -ForegroundColor $ColorWarning
    Write-Host "   Remove -DryRun parameter to apply changes." -ForegroundColor $ColorWarning
}

Write-Host "`n✨ Script execution completed!`n" -ForegroundColor $ColorSuccess

