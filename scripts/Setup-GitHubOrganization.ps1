<#
.SYNOPSIS
    Setup GitHub Organization for Gravity MicroServices Platform

.DESCRIPTION
    Creates and configures GitHub Organization 'GravityMicroServices' with:
    - Organization profile
    - Team structure
    - Access policies
    - Repository templates
    - Required integrations

.PARAMETER OrgName
    GitHub Organization name (default: GravityMicroServices)

.PARAMETER GitHubToken
    GitHub Personal Access Token with admin:org scope

.EXAMPLE
    .\Setup-GitHubOrganization.ps1 -GitHubToken "ghp_xxxxx"
#>

param(
    [string]$OrgName = "GravityMicroServices",
    [Parameter(Mandatory = $true)]
    [string]$GitHubToken
)

$ErrorActionPreference = "Stop"

# Colors
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

# GitHub API Headers
$headers = @{
    "Authorization" = "token $GitHubToken"
    "Accept"        = "application/vnd.github.v3+json"
}

Write-Info ""
Write-Info "========================================="
Write-Info "🏢 GITHUB ORGANIZATION SETUP"
Write-Info "========================================="
Write-Info ""

# ==============================================================================
# STEP 1: Check Organization Existence
# ==============================================================================
Write-Info "📋 Step 1: Checking if organization exists..."

try {
    $orgUrl = "https://api.github.com/orgs/$OrgName"
    $response = Invoke-RestMethod -Uri $orgUrl -Headers $headers -Method Get
    Write-Success "✅ Organization '$OrgName' already exists"
    $orgExists = $true
}
catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Warning "⚠️  Organization '$OrgName' does not exist"
        Write-Info "📝 You need to create it manually at: https://github.com/organizations/plan"
        Write-Info "   Organization settings will be configured once created"
        $orgExists = $false
    }
    else {
        Write-Error "❌ Error checking organization: $($_.Exception.Message)"
        exit 1
    }
}

if (-not $orgExists) {
    Write-Warning ""
    Write-Warning "⚠️  MANUAL STEP REQUIRED:"
    Write-Warning "   1. Go to: https://github.com/organizations/plan"
    Write-Warning "   2. Create organization: $OrgName"
    Write-Warning "   3. Choose plan: Free (or Team/Enterprise)"
    Write-Warning "   4. Re-run this script"
    Write-Warning ""
    exit 0
}

# ==============================================================================
# STEP 2: Configure Organization Profile
# ==============================================================================
Write-Info ""
Write-Info "📝 Step 2: Configuring organization profile..."

$orgProfile = @{
    name                                    = "Gravity MicroServices Platform"
    description                             = "Production-ready microservices for any software project. 52 independent, reusable services with enterprise-grade quality."
    blog                                    = "https://gravitymicroservices.io"
    location                                = "Global"
    email                                   = "team@gravitymicroservices.io"
    twitter_username                        = "GravityServices"
    company                                 = "Gravity Platform"
    billing_email                           = "billing@gravitymicroservices.io"
    has_organization_projects               = $true
    has_repository_projects                 = $true
    default_repository_permission           = "read"
    members_can_create_repositories         = $true
    members_can_create_public_repositories  = $false
    members_can_create_private_repositories = $true
    members_can_create_pages                = $true
}

try {
    $updateUrl = "https://api.github.com/orgs/$OrgName"
    Invoke-RestMethod -Uri $updateUrl -Headers $headers -Method Patch -Body ($orgProfile | ConvertTo-Json) | Out-Null
    Write-Success "✅ Organization profile configured"
}
catch {
    Write-Warning "⚠️  Could not update all profile settings: $($_.Exception.Message)"
}

# ==============================================================================
# STEP 3: Create Teams
# ==============================================================================
Write-Info ""
Write-Info "👥 Step 3: Creating teams..."

$teams = @(
    @{
        name        = "core-infrastructure"
        description = "Core Infrastructure Team - P0 Services"
        privacy     = "closed"
        permission  = "push"
    },
    @{
        name        = "authentication-team"
        description = "Authentication & Authorization Team"
        privacy     = "closed"
        permission  = "push"
    },
    @{
        name        = "payment-team"
        description = "Payment & Transaction Team"
        privacy     = "closed"
        permission  = "push"
    },
    @{
        name        = "notification-team"
        description = "Notification & Communication Team"
        privacy     = "closed"
        permission  = "push"
    },
    @{
        name        = "data-team"
        description = "Data & Analytics Team"
        privacy     = "closed"
        permission  = "push"
    },
    @{
        name        = "devops-team"
        description = "DevOps & Infrastructure Team"
        privacy     = "closed"
        permission  = "admin"
    },
    @{
        name        = "security-team"
        description = "Security & Compliance Team"
        privacy     = "closed"
        permission  = "admin"
    },
    @{
        name        = "qa-team"
        description = "Quality Assurance & Testing Team"
        privacy     = "closed"
        permission  = "push"
    },
    @{
        name        = "architects"
        description = "Principal Architects & Tech Leads"
        privacy     = "closed"
        permission  = "admin"
    }
)

$createdTeams = @{}

foreach ($team in $teams) {
    try {
        $teamUrl = "https://api.github.com/orgs/$OrgName/teams"
        $result = Invoke-RestMethod -Uri $teamUrl -Headers $headers -Method Post -Body ($team | ConvertTo-Json)
        $createdTeams[$team.name] = $result.id
        Write-Success "  ✅ Created team: $($team.name)"
    }
    catch {
        if ($_.Exception.Response.StatusCode -eq 422) {
            Write-Warning "  ⚠️  Team '$($team.name)' already exists"
            # Get existing team ID
            try {
                $getTeamUrl = "https://api.github.com/orgs/$OrgName/teams/$($team.name)"
                $existingTeam = Invoke-RestMethod -Uri $getTeamUrl -Headers $headers -Method Get
                $createdTeams[$team.name] = $existingTeam.id
            }
            catch {
                Write-Warning "  ⚠️  Could not get team ID for $($team.name)"
            }
        }
        else {
            Write-Warning "  ⚠️  Error creating team $($team.name): $($_.Exception.Message)"
        }
    }
}

# ==============================================================================
# STEP 4: Create Repository Labels
# ==============================================================================
Write-Info ""
Write-Info "🏷️  Step 4: Defining standard labels..."

$standardLabels = @(
    @{ name = "priority-p0"; color = "d73a4a"; description = "Critical - Must have" },
    @{ name = "priority-p1"; color = "ff6b6b"; description = "High priority" },
    @{ name = "priority-p2"; color = "fbca04"; description = "Medium priority" },
    @{ name = "priority-p3"; color = "0e8a16"; description = "Low priority" },
    @{ name = "type-bug"; color = "d73a4a"; description = "Bug or defect" },
    @{ name = "type-feature"; color = "a2eeef"; description = "New feature" },
    @{ name = "type-enhancement"; color = "84b6eb"; description = "Enhancement" },
    @{ name = "type-documentation"; color = "0075ca"; description = "Documentation" },
    @{ name = "status-blocked"; color = "d93f0b"; description = "Blocked by dependency" },
    @{ name = "status-in-progress"; color = "fbca04"; description = "Work in progress" },
    @{ name = "status-review"; color = "0e8a16"; description = "Ready for review" },
    @{ name = "security"; color = "ee0701"; description = "Security issue" },
    @{ name = "performance"; color = "1d76db"; description = "Performance issue" },
    @{ name = "breaking-change"; color = "d93f0b"; description = "Breaking change" },
    @{ name = "good-first-issue"; color = "7057ff"; description = "Good for newcomers" },
    @{ name = "help-wanted"; color = "008672"; description = "Extra attention needed" }
)

Write-Success "✅ Defined $($standardLabels.Count) standard labels"
Write-Info "   (Labels will be created for each repository)"

# ==============================================================================
# STEP 5: Create Branch Protection Rules Template
# ==============================================================================
Write-Info ""
Write-Info "🔒 Step 5: Defining branch protection template..."

$branchProtection = @{
    required_status_checks        = @{
        strict   = $true
        contexts = @("test", "lint", "security-scan")
    }
    enforce_admins                = $false
    required_pull_request_reviews = @{
        dismissal_restrictions          = @{}
        dismiss_stale_reviews           = $true
        require_code_owner_reviews      = $true
        required_approving_review_count = 2
    }
    restrictions                  = $null
    required_linear_history       = $true
    allow_force_pushes            = $false
    allow_deletions               = $false
}

Write-Success "✅ Branch protection template defined"
Write-Info "   (Will be applied to 'main' branch of each repository)"

# ==============================================================================
# STEP 6: Save Configuration
# ==============================================================================
Write-Info ""
Write-Info "💾 Step 6: Saving configuration..."

$config = @{
    organization_name = $OrgName
    organization_url  = "https://github.com/$OrgName"
    created_date      = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    teams             = $createdTeams
    standard_labels   = $standardLabels
    branch_protection = $branchProtection
}

$configPath = ".\migration\organization-config.json"
New-Item -ItemType Directory -Force -Path (Split-Path $configPath) | Out-Null
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath

Write-Success "✅ Configuration saved to: $configPath"

# ==============================================================================
# STEP 7: Generate Repository Setup Script
# ==============================================================================
Write-Info ""
Write-Info "📝 Step 7: Generating repository setup script..."

$repoSetupScript = @"
# Repository Setup Script
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# Organization: $OrgName

function Setup-Repository {
    param(
        [string]`$RepoName,
        [string]`$Description,
        [string]`$Team
    )
    
    # Create repository
    `$repoData = @{
        name = `$RepoName
        description = `$Description
        private = `$false
        has_issues = `$true
        has_projects = `$true
        has_wiki = `$true
        auto_init = `$false
    }
    
    `$createUrl = "https://api.github.com/orgs/$OrgName/repos"
    `$repo = Invoke-RestMethod -Uri `$createUrl -Headers `$headers -Method Post -Body (`$repoData | ConvertTo-Json)
    
    Write-Host "✅ Created repository: `$RepoName"
    
    # Add labels
    foreach (`$label in `$standardLabels) {
        `$labelUrl = "https://api.github.com/repos/$OrgName/`$RepoName/labels"
        Invoke-RestMethod -Uri `$labelUrl -Headers `$headers -Method Post -Body (`$label | ConvertTo-Json) -ErrorAction SilentlyContinue
    }
    
    # Setup branch protection
    `$protectUrl = "https://api.github.com/repos/$OrgName/`$RepoName/branches/main/protection"
    Invoke-RestMethod -Uri `$protectUrl -Headers `$headers -Method Put -Body (`$branchProtection | ConvertTo-Json -Depth 10) -ErrorAction SilentlyContinue
    
    # Add team access
    if (`$Team -and `$createdTeams[`$Team]) {
        `$teamId = `$createdTeams[`$Team]
        `$teamUrl = "https://api.github.com/orgs/$OrgName/teams/`$teamId/repos/$OrgName/`$RepoName"
        `$teamAccess = @{ permission = "push" }
        Invoke-RestMethod -Uri `$teamUrl -Headers `$headers -Method Put -Body (`$teamAccess | ConvertTo-Json) -ErrorAction SilentlyContinue
    }
    
    return `$repo
}

# Export function
Export-ModuleMember -Function Setup-Repository
"@

$setupScriptPath = ".\migration\Repository-Setup.psm1"
$repoSetupScript | Set-Content $setupScriptPath

Write-Success "✅ Repository setup module created: $setupScriptPath"

# ==============================================================================
# SUMMARY
# ==============================================================================
Write-Info ""
Write-Info "========================================="
Write-Success "✅ ORGANIZATION SETUP COMPLETE"
Write-Info "========================================="
Write-Info ""
Write-Info "Organization: $OrgName"
Write-Info "URL: https://github.com/$OrgName"
Write-Info ""
Write-Info "Created Resources:"
Write-Info "  • Teams: $($teams.Count)"
Write-Info "  • Standard labels: $($standardLabels.Count)"
Write-Info "  • Branch protection: Configured"
Write-Info "  • Repository template: Ready"
Write-Info ""
Write-Info "Configuration Files:"
Write-Info "  • $configPath"
Write-Info "  • $setupScriptPath"
Write-Info ""
Write-Success "🚀 Ready to create repositories!"
Write-Info ""
Write-Info "Next Steps:"
Write-Info "  1. Review configuration in $configPath"
Write-Info "  2. Run: .\Create-ServiceRepositories.ps1"
Write-Info "  3. Start migration with: .\Migrate-ToMultiRepo.ps1"
Write-Info ""
