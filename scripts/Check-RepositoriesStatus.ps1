<#
.SYNOPSIS
    Check status of all Gravity repositories

.DESCRIPTION
    Shows git status, branch, and last commit for all repositories

.PARAMETER RepositoriesDirectory
    Directory containing all cloned repositories

.EXAMPLE
    .\Check-RepositoriesStatus.ps1 -RepositoriesDirectory "C:\Projects\Gravity"

.NOTES
    Author: Gravity Elite Engineering Team
    Version: 1.0.0
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoriesDirectory
)

$ErrorActionPreference = "Continue"

function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }

Write-Info "Checking status of all repositories..."

# Find all gravity-* directories
$Repositories = Get-ChildItem -Path $RepositoriesDirectory -Directory -Filter "gravity-*"

$Results = @()

foreach ($repo in $Repositories) {
    Push-Location $repo.FullName
    
    $Branch = git branch --show-current
    $Status = git status --porcelain
    $LastCommit = git log -1 --pretty=format:"%h - %s (%cr)"
    $BehindAhead = git rev-list --left-right --count origin/$Branch...$Branch 2>$null
    
    $Result = [PSCustomObject]@{
        Repository  = $repo.Name
        Branch      = $Branch
        Modified    = ($Status -ne $null -and $Status -ne "")
        LastCommit  = $LastCommit
        BehindAhead = $BehindAhead
    }
    
    $Results += $Result
    
    Pop-Location
}

# Display results
Write-Host ""
Write-Host "Repository Status Summary" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan

foreach ($result in $Results) {
    Write-Host ""
    Write-Host "Repository: $($result.Repository)" -ForegroundColor Yellow
    Write-Host "  Branch: $($result.Branch)" -ForegroundColor White
    
    if ($result.Modified) {
        Write-Host "  Status: Modified (uncommitted changes)" -ForegroundColor Red
    }
    else {
        Write-Host "  Status: Clean" -ForegroundColor Green
    }
    
    Write-Host "  Last Commit: $($result.LastCommit)" -ForegroundColor Gray
    
    if ($result.BehindAhead) {
        Write-Host "  Sync: $($result.BehindAhead)" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Info "Status check completed!"
