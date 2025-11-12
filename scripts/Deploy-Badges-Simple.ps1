#!/usr/bin/env pwsh
param([int]$Start = 1)

$services = 1..52 | ForEach-Object { "{0:D2}-{1}" -f $_, @(
        "common-library", "service-discovery", "api-gateway", "config-service",
        "auth-service", "user-service", "notification-service", "email-service",
        "sms-service", "file-storage-service", "permission-service", "session-service",
        "audit-log-service", "cache-service", "payment-service", "order-service",
        "product-service", "cart-service", "search-service", "recommendation-service",
        "review-service", "wishlist-service", "analytics-service", "reporting-service",
        "inventory-service", "shipping-service", "invoice-service", "chat-service",
        "video-call-service", "geolocation-service", "subscription-service", "loyalty-service",
        "coupon-service", "referral-service", "translation-service", "cms-service",
        "feedback-service", "monitoring-service", "logging-service", "scheduler-service",
        "webhook-service", "export-service", "import-service", "backup-service",
        "rate-limiter-service", "ab-testing-service", "feature-flag-service", "tax-service",
        "fraud-detection-service", "kyc-service", "gamification-service", "social-media-service"
    )[$_ - 1] }

Write-Host "`n🎨 README BADGES DEPLOYMENT - Starting from #$Start" -ForegroundColor Cyan
$ok = 0; $skip = 0

foreach ($svc in $services[($Start - 1)..51]) {
    try {
        $tmp = Join-Path $env:TEMP "badge$(Get-Random)"
        gh repo clone "Shakour-Data/$svc" $tmp 2>&1 | Out-Null
        
        $readme = Join-Path $tmp "README.md"
        if (-not (Test-Path $readme)) {
            # Create minimal README if doesn't exist
            @"
# $svc

[![CI](https://github.com/Shakour-Data/$svc/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/$svc/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/$svc/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/$svc/actions/workflows/cd.yml)

Part of the GravityWaves microservices ecosystem.
"@ | Out-File -FilePath $readme -Encoding UTF8
            $action = "created"
        }
        else {
            $content = Get-Content $readme -Raw
            if ($content -match '!\[CI\].*actions/workflows/ci\.yml') {
                Write-Host "  ✓ $svc (skip - badges exist)" -ForegroundColor Gray
                Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
                $skip++
                continue
            }
            
            # Insert badges at top (after title if exists)
            $badges = @"
[![CI](https://github.com/Shakour-Data/$svc/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/$svc/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/$svc/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/$svc/actions/workflows/cd.yml)

"@
            if ($content -match '^#\s+(.+)$') {
                $content = $content -replace '^(#\s+.+\r?\n)', "`$1`n$badges"
            }
            else {
                $content = "$badges`n$content"
            }
            $content | Out-File -FilePath $readme -Encoding UTF8
            $action = "updated"
        }
        
        Push-Location $tmp
        git add README.md 2>&1 | Out-Null
        git commit -m "docs: add CI/CD badges to README" 2>&1 | Out-Null
        $pushOutput = git push origin main 2>&1 | Out-String
        $pushOK = ($pushOutput -notmatch "fatal") -and ($pushOutput -match "main -> main")
        Pop-Location
        
        Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
        
        if ($pushOK) {
            Write-Host "  ✅ $svc ($action)" -ForegroundColor Green
            $ok++
        }
        else {
            Write-Host "  ⚠️ $svc (push failed)" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  ❌ $svc : $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n📊 Results: ✅ $ok | ⏭️  $skip skipped`n" -ForegroundColor $(if ($ok -gt 40) { 'Green' }else { 'Yellow' })
