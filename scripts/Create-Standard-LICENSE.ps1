#Requires -Version 7.0

<#
.SYNOPSIS
    Create standardized LICENSE files for all Gravity MicroServices
.DESCRIPTION
    Generates MIT License files for each service with consistent:
    - Copyright year (2025)
    - Copyright holder (Gravity MicroServices Platform)
    - Standard MIT License text
.PARAMETER StartFrom
    Service number to start from (default: 4)
.PARAMETER EndAt
    Service number to end at (default: 52)
.PARAMETER DryRun
    If specified, only shows what would be done without creating files
.EXAMPLE
    .\Create-Standard-LICENSE.ps1
    .\Create-Standard-LICENSE.ps1 -StartFrom 4 -EndAt 10
    .\Create-Standard-LICENSE.ps1 -DryRun
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

function New-LicenseContent {
    return @"
MIT License

Copyright (c) 2025 Gravity MicroServices Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@
}

# Main script execution
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  LICENSE Files Generation for Gravity MicroServices" -ForegroundColor Cyan
Write-Host "  Range: Service $StartFrom to $EndAt" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

$created = 0
$updated = 0
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
    $serviceDir = "$serviceNumber-$serviceName"
    $servicePath = Join-Path $PSScriptRoot ".." $serviceDir
    $licensePath = Join-Path $servicePath "LICENSE"
    
    Write-Host "[$i/$EndAt] $serviceDir " -NoNewline
    
    if (-not (Test-Path $servicePath)) {
        Write-Host "❌ Service directory not found" -ForegroundColor Red
        $errors++
        continue
    }
    
    if ($DryRun) {
        if (Test-Path $licensePath) {
            Write-Host "🔍 Would update LICENSE" -ForegroundColor Yellow
            $updated++
        }
        else {
            Write-Host "🔍 Would create LICENSE" -ForegroundColor Yellow
            $created++
        }
        continue
    }
    
    try {
        $licenseContent = New-LicenseContent
        $exists = Test-Path $licensePath
        
        $licenseContent | Out-File -FilePath $licensePath -Encoding UTF8 -NoNewline
        
        if ($exists) {
            Write-Host "✅ LICENSE updated" -ForegroundColor Green
            $updated++
        }
        else {
            Write-Host "✅ LICENSE created" -ForegroundColor Green
            $created++
        }
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Created: $created" -ForegroundColor Green
Write-Host "  Updated: $updated" -ForegroundColor Cyan
Write-Host "  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "  Errors:  $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })

if ($DryRun) {
    Write-Host "`nℹ️  This was a DRY RUN. Use without -DryRun to create/update files." -ForegroundColor Yellow
}

Write-Host "================================================================`n" -ForegroundColor Cyan
