# Gravity Multi-Repo Migration Guide

> **Complete guide for migrating from monorepo to multi-repo architecture**

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Pre-Migration Checklist](#pre-migration-checklist)
4. [Step-by-Step Migration Process](#step-by-step-migration-process)
5. [Post-Migration Tasks](#post-migration-tasks)
6. [Team Onboarding](#team-onboarding)
7. [Troubleshooting](#troubleshooting)
8. [Rollback Procedures](#rollback-procedures)
9. [FAQ](#faq)

---

## Overview

### Migration Strategy

We are migrating from a **monorepo** (single repository containing all 52 services) to a **multi-repo** architecture (52 independent repositories) based on unanimous team consensus.

### Benefits

- ✅ **True Independence**: Each service has its own repository, CI/CD, and versioning
- ✅ **Security Isolation**: Breaches are contained to individual repositories
- ✅ **CI/CD Speed**: 5-10 minutes vs 45-60 minutes
- ✅ **Clear Versioning**: Semantic versioning per service
- ✅ **Team Autonomy**: Each team owns their repositories
- ✅ **Better Reusability**: Services can be used in other projects

### Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| **Phase 1: Preparation** | Week 1 | Setup GitHub org, create templates |
| **Phase 2: Pilot Migration** | Week 2 | Migrate 2-3 services for testing |
| **Phase 3: P0 Services** | Week 3 | Migrate critical infrastructure (01-04) |
| **Phase 4: P1 Services** | Week 4-5 | Migrate primary services (05-14) |
| **Phase 5: P2-P4 Services** | Week 6-8 | Migrate remaining services (15-52) |
| **Phase 6: Verification** | Week 9 | Full testing and validation |

---

## Prerequisites

### Required Tools

```powershell
# Check Git version (requires 2.20+)
git --version

# Check PowerShell version (requires 5.1+)
$PSVersionTable.PSVersion

# Install GitHub CLI (optional but recommended)
winget install GitHub.cli
```

### Access Requirements

1. **GitHub Access**
   - Admin access to `GravityMicroServices` organization
   - Personal Access Token with `repo` and `admin:org` scopes
   - Generate at: https://github.com/settings/tokens

2. **Local Environment**
   - Git configured with SSH keys
   - PowerShell 5.1 or higher
   - At least 10GB free disk space

3. **Permissions**
   - Write access to current monorepo
   - Ability to create repositories in GitHub org
   - Access to CI/CD secrets and credentials

### Creating GitHub Token

```powershell
# Navigate to GitHub Settings > Developer Settings > Personal Access Tokens
# Click "Generate new token (classic)"
# Select scopes:
#   - repo (full control)
#   - admin:org (full control)
#   - delete_repo (if needed for cleanup)
# Copy the token securely
```

---

## Pre-Migration Checklist

### 1. Backup Current State

```powershell
# Create full backup of monorepo
$BackupPath = "E:\Backups\GravityMicroServices-$(Get-Date -Format 'yyyyMMdd')"
Copy-Item -Path "E:\Shakour\GravityMicroServices" -Destination $BackupPath -Recurse
```

### 2. Verify All Services

```powershell
# Check all services are present
Get-ChildItem -Path "E:\Shakour\GravityMicroServices" -Directory | Where-Object { $_.Name -match '^\d{2}-' }
```

### 3. Test Template Repository

```powershell
# Verify template is complete
Test-Path "E:\Shakour\GravityMicroServices\gravity-template-service"

# Check template structure
Get-ChildItem "E:\Shakour\GravityMicroServices\gravity-template-service" -Recurse | Select-Object FullName
```

### 4. Document Current State

- [ ] List all active branches
- [ ] Document open pull requests
- [ ] Record current CI/CD pipelines
- [ ] Note any custom configurations
- [ ] Export environment variables

---

## Step-by-Step Migration Process

### Step 1: Setup GitHub Organization

**Duration:** 30 minutes

```powershell
# Navigate to scripts directory
cd E:\Shakour\GravityMicroServices\scripts

# Run organization setup script
.\Setup-GitHubOrganization.ps1 `
    -OrgName "GravityMicroServices" `
    -GitHubToken "YOUR_GITHUB_TOKEN"
```

**Verify:**
- ✅ Organization profile updated
- ✅ 9 teams created
- ✅ 16 labels defined
- ✅ Branch protection rules active
- ✅ Configuration file generated

### Step 2: Pilot Migration (Test with 2-3 Services)

**Duration:** 2-3 hours

Start with these services for testing:
1. `01-common-library` (P0, foundational)
2. `05-auth-service` (P1, well-tested)
3. `07-notification-service` (P1, simple)

```powershell
# Migrate first pilot service
.\Migrate-Service.ps1 `
    -ServiceNumber "01" `
    -ServiceName "common-library" `
    -GitHubToken "YOUR_GITHUB_TOKEN"

# Verify repository
Start-Process "https://github.com/GravityMicroServices/gravity-common-library"

# Test CI/CD
git clone https://github.com/GravityMicroServices/gravity-common-library.git
cd gravity-common-library
# Make a small change and push to test CI
```

**Validation Checklist:**
- [ ] Repository created successfully
- [ ] All files present
- [ ] CI/CD workflow running
- [ ] Tests passing
- [ ] Docker image building
- [ ] No security vulnerabilities
- [ ] Labels applied
- [ ] Branch protection active
- [ ] Team assigned

### Step 3: Migrate P0 Services (Critical Infrastructure)

**Duration:** 1 day

```powershell
# Migrate P0 services (01-04)
$P0Services = @(
    @{Number="01"; Name="common-library"},
    @{Number="02"; Name="service-discovery"},
    @{Number="03"; Name="api-gateway"},
    @{Number="04"; Name="config-server"}
)

foreach ($service in $P0Services) {
    Write-Host "Migrating $($service.Number)-$($service.Name)..." -ForegroundColor Cyan
    
    .\Migrate-Service.ps1 `
        -ServiceNumber $service.Number `
        -ServiceName $service.Name `
        -GitHubToken "YOUR_GITHUB_TOKEN"
    
    # Wait before next migration to avoid rate limiting
    Start-Sleep -Seconds 5
}
```

### Step 4: Migrate P1 Services (Primary Services)

**Duration:** 2 days

```powershell
# Migrate P1 services (05-14)
.\Migrate-AllServices.ps1 `
    -GitHubToken "YOUR_GITHUB_TOKEN" `
    -StartFrom 5 `
    -EndAt 14
```

### Step 5: Migrate Remaining Services (P2-P4)

**Duration:** 3-4 days

```powershell
# Migrate all remaining services
.\Migrate-AllServices.ps1 `
    -GitHubToken "YOUR_GITHUB_TOKEN" `
    -StartFrom 15 `
    -EndAt 52
```

### Step 6: Update Common Library for PyPI

**Duration:** 4 hours

```powershell
# Clone common library
git clone https://github.com/GravityMicroServices/gravity-common-library.git
cd gravity-common-library

# Update pyproject.toml for PyPI
# Add build configuration
# Test build
poetry build

# Publish to PyPI (test first)
poetry publish --repository testpypi

# Then publish to production PyPI
poetry publish
```

### Step 7: Update All Services to Use PyPI Package

```powershell
# Update each service's pyproject.toml
# Change from:
#   gravity-common = { path = "../01-common-library" }
# To:
#   gravity-common = "^1.0.0"

# Run update script
.\Update-AllRepositories.ps1 -RepositoriesDirectory "C:\Projects\Gravity"
```

---

## Post-Migration Tasks

### 1. Verify All Repositories

```powershell
# Clone all repositories
.\Clone-AllRepositories.ps1 -TargetDirectory "C:\Projects\Gravity"

# Check status of all repositories
.\Check-RepositoriesStatus.ps1 -RepositoriesDirectory "C:\Projects\Gravity"
```

### 2. Update Documentation

- [ ] Update README.md in each repository
- [ ] Update architecture diagrams
- [ ] Update team wiki pages
- [ ] Create repository index
- [ ] Document new workflows

### 3. Configure CI/CD Secrets

For each repository:

```bash
# Add secrets via GitHub CLI
gh secret set DATABASE_URL --repo GravityMicroServices/gravity-{service}
gh secret set REDIS_URL --repo GravityMicroServices/gravity-{service}
gh secret set SECRET_KEY --repo GravityMicroServices/gravity-{service}
```

### 4. Setup Team Permissions

```powershell
# Assign teams to repositories
# This can be automated via GitHub API
```

### 5. Archive Monorepo

```powershell
# Archive the monorepo (DO NOT DELETE)
# 1. Push final commit documenting migration
# 2. Mark repository as archived on GitHub
# 3. Update README with migration notice
# 4. Keep for historical reference
```

---

## Team Onboarding

### For Developers

#### Getting Started

```bash
# 1. Clone your team's repositories
git clone https://github.com/GravityMicroServices/gravity-{your-service}.git

# 2. Install dependencies
cd gravity-{your-service}
poetry install

# 3. Copy environment template
cp .env.example .env

# 4. Run service
docker-compose up -d
poetry run uvicorn app.main:app --reload
```

#### Daily Workflow

```bash
# Update your service
git pull origin main

# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git add .
git commit -m "feat: your feature"

# Push and create PR
git push origin feature/your-feature
gh pr create --title "Your Feature" --body "Description"
```

#### Working with Multiple Services

```powershell
# Clone all services you need
.\Clone-AllRepositories.ps1 -TargetDirectory "C:\Projects\Gravity"

# Update all services
.\Update-AllRepositories.ps1 -RepositoriesDirectory "C:\Projects\Gravity"

# Check status across all services
.\Check-RepositoriesStatus.ps1 -RepositoriesDirectory "C:\Projects\Gravity"
```

### For Team Leads

#### Managing Your Team's Repositories

1. **Access Control**
   - Team members have push access
   - Set up branch protection
   - Configure CODEOWNERS

2. **Monitoring**
   - Watch CI/CD workflows
   - Review pull requests
   - Monitor deployment status

3. **Coordination**
   - Use project boards
   - Regular sync meetings
   - Document decisions in repo issues

---

## Troubleshooting

### Common Issues

#### Issue 1: Migration Script Fails

**Symptoms:** Script exits with error, repository not created

**Solutions:**
```powershell
# Check GitHub token
echo $env:GITHUB_TOKEN

# Verify token scopes at https://github.com/settings/tokens

# Check rate limiting
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit

# Re-run with dry-run first
.\Migrate-Service.ps1 -ServiceNumber "XX" -ServiceName "service-name" -GitHubToken "TOKEN" -DryRun
```

#### Issue 2: CI/CD Workflow Fails

**Symptoms:** GitHub Actions fail, tests don't run

**Solutions:**
```bash
# Check workflow file
cat .github/workflows/ci.yml

# Verify secrets are set
gh secret list --repo GravityMicroServices/gravity-{service}

# Check logs
gh run list --repo GravityMicroServices/gravity-{service}
gh run view {run-id} --log

# Re-trigger workflow
gh workflow run ci.yml --repo GravityMicroServices/gravity-{service}
```

#### Issue 3: Missing Dependencies

**Symptoms:** Import errors, module not found

**Solutions:**
```bash
# Update common library
poetry add gravity-common@latest

# Or install from local path temporarily
poetry add ../gravity-common-library

# Rebuild dependencies
poetry lock
poetry install
```

#### Issue 4: Rate Limiting

**Symptoms:** API calls fail with 403 errors

**Solutions:**
```powershell
# Check rate limit status
Invoke-RestMethod -Uri "https://api.github.com/rate_limit" -Headers @{
    "Authorization" = "token YOUR_TOKEN"
}

# Wait for rate limit reset
# Or use different token
# Or add delays between operations
```

---

## Rollback Procedures

### If Migration Needs to be Reversed

#### Step 1: Stop All New Commits

```powershell
# Immediately notify all teams
# Set all repositories to archived (read-only)
```

#### Step 2: Restore from Backup

```powershell
# Restore monorepo backup
$BackupPath = "E:\Backups\GravityMicroServices-20240101"
Copy-Item -Path $BackupPath -Destination "E:\Shakour\GravityMicroServices" -Recurse -Force
```

#### Step 3: Resume Operations

```powershell
# Re-enable CI/CD on monorepo
# Notify teams to use monorepo
# Document lessons learned
```

#### Step 4: Plan Re-Migration

- Analyze what went wrong
- Fix issues in scripts/templates
- Test more thoroughly
- Schedule new migration

---

## FAQ

### Q: Can I delete the monorepo after migration?

**A:** No, keep it archived for at least 6 months as a reference and backup.

### Q: What if a service needs changes during migration?

**A:** Complete migration first, then make changes in the new repository. Don't mix migration with feature development.

### Q: How do we handle shared code?

**A:** All shared code goes in `gravity-common-library` published to PyPI. Services import it as a dependency.

### Q: What about database migrations?

**A:** Each service keeps its own Alembic migrations. No changes needed.

### Q: How do we coordinate releases across services?

**A:** Use semantic versioning and maintain a release calendar. Services are deployed independently.

### Q: What if CI/CD fails for a service?

**A:** Fix in the new repository. CI/CD templates are included, but may need adjustments per service.

### Q: Can we migrate back to monorepo?

**A:** Technically yes, but very complex. The multi-repo benefits outweigh the challenges.

### Q: How do we handle inter-service dependencies?

**A:** Services communicate via REST APIs and events. No source-level dependencies except `gravity-common`.

---

## Support

### Getting Help

1. **Documentation**: Check this guide first
2. **Team Chat**: Ask in #gravity-migration channel
3. **GitHub Issues**: Report bugs in migration scripts
4. **Architecture Team**: Contact for complex issues

### Resources

- **Migration Scripts**: `scripts/` directory
- **Template Repository**: `gravity-template-service/`
- **Architecture Docs**: `docs/COMPLETE_ARCHITECTURE.md`
- **Team Decision**: `docs/GIT_STRATEGY_DECISION.md`

---

**Built with ❤️ by the Gravity Elite Engineering Team**

*Last Updated: 2024*
