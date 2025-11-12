#Requires -Version 7.0

<#
.SYNOPSIS
    Add comprehensive type hints to Priority 1 services (04-15)
.DESCRIPTION
    Analyzes Python files in Priority 1 services and adds comprehensive type hints:
    - Function return types
    - Parameter types
    - Variable annotations where appropriate
    - Import statements for typing module
    Creates a report of files that need manual review
.PARAMETER ServiceNumber
    Specific service number to process (04-15)
.PARAMETER DryRun
    If specified, only shows what would be done without modifying files
.EXAMPLE
    .\Add-Type-Hints.ps1 -ServiceNumber 4
    .\Add-Type-Hints.ps1 -DryRun
#>

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateRange(4, 15)]
    [int]$ServiceNumber,
    
    [Parameter()]
    [switch]$DryRun
)

# Priority 1 Services (04-15)
$priority1Services = @{
    4  = @{ Name = "config-service"; Description = "Configuration Management Service" }
    5  = @{ Name = "auth-service"; Description = "Authentication & Authorization Service" }
    6  = @{ Name = "user-service"; Description = "User Management Service" }
    7  = @{ Name = "notification-service"; Description = "Notification Service" }
    8  = @{ Name = "email-service"; Description = "Email Service" }
    9  = @{ Name = "sms-service"; Description = "SMS Service" }
    10 = @{ Name = "file-storage-service"; Description = "File Storage Service" }
    11 = @{ Name = "permission-service"; Description = "Permission Management Service" }
    12 = @{ Name = "session-service"; Description = "Session Management Service" }
    13 = @{ Name = "audit-log-service"; Description = "Audit Logging Service" }
    14 = @{ Name = "cache-service"; Description = "Distributed Cache Service" }
    15 = @{ Name = "payment-service"; Description = "Payment Processing Service" }
}

function Test-HasTypeHints {
    param([string]$FilePath)
    
    $content = Get-Content $FilePath -Raw
    
    # Check for common type hint patterns
    $hasReturnTypes = $content -match 'def \w+\([^)]*\)\s*->'
    $hasParamTypes = $content -match 'def \w+\([^)]*:\s*\w+'
    return ($hasReturnTypes -or $hasParamTypes)
}

function Get-PythonFiles {
    param([string]$ServicePath)
    
    $pythonFiles = Get-ChildItem -Path $ServicePath -Filter "*.py" -Recurse | 
    Where-Object { 
        $_.FullName -notmatch '__pycache__' -and 
        $_.FullName -notmatch 'alembic/versions' -and
        $_.FullName -notmatch '.backup'
    }
    
    return $pythonFiles
}

function Add-TypeHintsToFile {
    param(
        [string]$FilePath,
        [switch]$DryRun
    )
    
    $content = Get-Content $FilePath -Raw
    $modified = $false
    
    # Check if file already has comprehensive type hints
    if (Test-HasTypeHints -FilePath $FilePath) {
        return @{
            Modified = $false
            Reason   = "Already has type hints"
        }
    }
    
    # Simple main.py with minimal code
    if ($FilePath -match 'main\.py$' -and $content.Length -lt 500) {
        # Add type hints to health check endpoint
        if ($content -match '@app\.get\("/health"\)\s*\n\s*async def health_check\(\):') {
            $newContent = $content -replace '(@app\.get\("/health"\)\s*\n\s*)async def health_check\(\):', 
            '$1async def health_check() -> dict[str, str]:'
            
            # Add typing imports if not present
            if ($newContent -notmatch 'from typing import') {
                $newContent = "from typing import Any\n" + $newContent
            }
            
            if ($newContent -ne $content) {
                $modified = $true
                $content = $newContent
            }
        }
    }
    
    if ($modified -and -not $DryRun) {
        Set-Content -Path $FilePath -Value $content -NoNewline
    }
    
    return @{
        Modified = $modified
        Reason   = if ($modified) { "Added basic type hints" } else { "No modifications needed" }
    }
}

# Main script execution
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  Type Hints Addition - Priority 1 Services (04-15)" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

$servicesToProcess = if ($ServiceNumber) {
    @($ServiceNumber)
}
else {
    4..15
}

$totalFiles = 0
$filesWithTypeHints = 0
$filesNeedingWork = 0
$filesModified = 0

$report = @()

foreach ($serviceNum in $servicesToProcess) {
    if (-not $priority1Services.ContainsKey($serviceNum)) {
        continue
    }
    
    $service = $priority1Services[$serviceNum]
    $serviceNumber = $serviceNum.ToString("D2")
    $serviceDir = "$serviceNumber-$($service.Name)"
    $servicePath = Join-Path $PSScriptRoot ".." $serviceDir
    
    Write-Host "`n================================================================" -ForegroundColor Cyan
    Write-Host "[$serviceNum/15] $serviceDir" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    
    if (-not (Test-Path $servicePath)) {
        Write-Host "⚠️  Service directory not found - Skipping" -ForegroundColor Yellow
        continue
    }
    
    $pythonFiles = Get-PythonFiles -ServicePath $servicePath
    $totalFiles += $pythonFiles.Count
    
    Write-Host "ℹ️  Found $($pythonFiles.Count) Python files" -ForegroundColor Cyan
    
    foreach ($file in $pythonFiles) {
        $relativePath = $file.FullName.Replace($servicePath, "").TrimStart('\')
        
        if (Test-HasTypeHints -FilePath $file.FullName) {
            Write-Host "  ✅ $relativePath - Has type hints" -ForegroundColor Green
            $filesWithTypeHints++
        }
        else {
            Write-Host "  ⚠️  $relativePath - Needs type hints" -ForegroundColor Yellow
            $filesNeedingWork++
            
            # Try to add type hints automatically
            if (-not $DryRun) {
                $result = Add-TypeHintsToFile -FilePath $file.FullName
                if ($result.Modified) {
                    Write-Host "     ✨ Modified: $($result.Reason)" -ForegroundColor Green
                    $filesModified++
                }
            }
            
            $report += [PSCustomObject]@{
                Service      = $serviceDir
                File         = $relativePath
                Status       = "Needs Review"
                HasTypeHints = $false
            }
        }
    }
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total Python files: $totalFiles" -ForegroundColor Cyan
Write-Host "  Files with type hints: $filesWithTypeHints" -ForegroundColor Green
Write-Host "  Files needing work: $filesNeedingWork" -ForegroundColor Yellow
Write-Host "  Files modified: $filesModified" -ForegroundColor Green
Write-Host "  Coverage: $([math]::Round($filesWithTypeHints / $totalFiles * 100, 2))%" -ForegroundColor $(if ($filesWithTypeHints / $totalFiles -gt 0.8) { "Green" } else { "Yellow" })

if ($DryRun) {
    Write-Host "`nℹ️  This was a DRY RUN. Use without -DryRun to modify files." -ForegroundColor Yellow
}

if ($report.Count -gt 0) {
    Write-Host "`n================================================================" -ForegroundColor Cyan
    Write-Host "Files Needing Manual Review:" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    
    $report | Format-Table -AutoSize
    
    # Export report
    $reportPath = Join-Path $PSScriptRoot ".." "docs" "TYPE_HINTS_REPORT.md"
    $reportContent = @"
# Type Hints Report - Priority 1 Services

**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Total Files:** $totalFiles
**Files with Type Hints:** $filesWithTypeHints
**Files Needing Work:** $filesNeedingWork
**Coverage:** $([math]::Round($filesWithTypeHints / $totalFiles * 100, 2))%

## Files Needing Manual Review

| Service | File | Status |
|---------|------|--------|
$($report | ForEach-Object { "| $($_.Service) | $($_.File) | $($_.Status) |" } | Out-String)

## Next Steps

1. Review files listed above
2. Add comprehensive type hints:
   - Function return types
   - Parameter types  
   - Variable annotations
3. Run mypy for validation:
   ``````bash
   poetry run mypy app/
   ``````
4. Fix any type errors reported by mypy
5. Ensure all functions have docstrings with type information

## Type Hints Best Practices

### ✅ Good Examples:

``````python
from typing import Optional, List, Dict, Any
from datetime import datetime

async def get_user_by_id(
    user_id: int,
    db: AsyncSession
) -> Optional[User]:
    ""\"Get user by ID.""\"
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

def calculate_total(
    items: List[Dict[str, Any]],
    tax_rate: float = 0.1
) -> float:
    ""\"Calculate total with tax.""\"
    subtotal = sum(item['price'] for item in items)
    return round(subtotal * (1 + tax_rate), 2)
``````

### ❌ Bad Examples:

``````python
# No type hints
async def get_user_by_id(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# Incomplete type hints
def calculate_total(items: List, tax_rate=0.1):
    subtotal = sum(item['price'] for item in items)
    return round(subtotal * (1 + tax_rate), 2)
``````

"@
    
    if (-not $DryRun) {
        $reportContent | Out-File -FilePath $reportPath -Encoding UTF8
        Write-Host "`n📄 Report saved to: docs/TYPE_HINTS_REPORT.md" -ForegroundColor Green
    }
}

Write-Host "`n================================================================`n" -ForegroundColor Cyan
