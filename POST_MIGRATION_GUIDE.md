# 🚀 Post-Migration Setup Guide

## ✅ Migration Complete!

همه 52 سرویس با موفقیت به GitHub Organization منتقل شدند:
- **Organization**: https://github.com/GravityWavesGenerlServices
- **Archive**: https://github.com/Shakour-Data/GravityMicroServices-Archive

---

## 📋 Next Steps Checklist

### 1. ✅ Branch Protection (Completed ✓)

**Setup Script**: `scripts/Setup-BranchProtection.ps1`

```powershell
# Test first (Dry Run)
.\scripts\Setup-BranchProtection.ps1 -DryRun

# Apply to all repositories
.\scripts\Setup-BranchProtection.ps1
```

**Protection Rules**:
- ✅ Require pull request reviews (1 approval)
- ✅ Dismiss stale reviews on new commits
- ✅ Require status checks to pass
- ✅ Require conversation resolution
- ✅ No force pushes or deletions

---

### 2. 🔄 CI/CD Setup

**Setup Script**: `scripts/Add-GitHubActionsWorkflows.ps1`

```powershell
# Test first (Dry Run)
.\scripts\Add-GitHubActionsWorkflows.ps1 -DryRun

# Add CI only
.\scripts\Add-GitHubActionsWorkflows.ps1 -WorkflowType CI

# Add CD only
.\scripts\Add-GitHubActionsWorkflows.ps1 -WorkflowType CD

# Add both CI and CD
.\scripts\Add-GitHubActionsWorkflows.ps1 -WorkflowType Both
```

**CI Workflow** (`.github/workflows/ci.yml`):
- ✅ Run on push/PR to main/develop
- ✅ Setup Python 3.12
- ✅ Install dependencies
- ✅ Run linting (black, isort, mypy)
- ✅ Run security checks (bandit, safety)
- ✅ Run tests with coverage (min 80%)
- ✅ Upload coverage to Codecov

**CD Workflow** (`.github/workflows/cd.yml`):
- ✅ Run on push to main
- ✅ Build Docker image
- ✅ Push to Docker Hub
- ✅ Deploy to production (placeholder)

---

### 3. 👥 Team Access Management

#### Option A: Using GitHub CLI

```powershell
# Create team
gh api /orgs/GravityWavesGenerlServices/teams -f name="Backend Developers" -f privacy="closed"

# Add members to team
gh api /orgs/GravityWavesGenerlServices/teams/backend-developers/memberships/USERNAME -X PUT

# Give team access to all repositories
$repos = gh repo list GravityWavesGenerlServices --limit 100 --json name -q '.[].name'
foreach ($repo in $repos) {
    gh api /orgs/GravityWavesGenerlServices/teams/backend-developers/repos/GravityWavesGenerlServices/$repo `
        -X PUT -f permission="push"
}
```

#### Option B: Using GitHub Web Interface

1. Go to: https://github.com/orgs/GravityWavesGenerlServices/teams
2. Click "New team"
3. Set team name: "Backend Developers"
4. Add team members
5. Grant repository access:
   - Go to each repository → Settings → Manage access
   - Add team with appropriate permissions

**Recommended Permission Levels**:
- **Admin**: Full access (repository owners)
- **Write**: Push, PR merge (developers)
- **Read**: View only (QA, stakeholders)

---

### 4. 📚 Documentation Updates

#### Update README files:

```powershell
# For each service, update links
$services = gh repo list GravityWavesGenerlServices --limit 100 --json name -q '.[].name'

foreach ($service in $services) {
    Write-Host "Updating $service..."
    # Clone, update README, commit, push
}
```

**Things to update in each README**:
- ✅ Organization URL
- ✅ Repository URL
- ✅ CI/CD badge status
- ✅ Coverage badge
- ✅ Quick start guide
- ✅ Deployment instructions

---

### 5. 🔐 Secrets Management

**Required Secrets** (for each repository):

```powershell
# Add secrets to repository
gh secret set DOCKER_USERNAME -R GravityWavesGenerlServices/01-common-library
gh secret set DOCKER_PASSWORD -R GravityWavesGenerlServices/01-common-library

# Database secrets
gh secret set DATABASE_URL -R GravityWavesGenerlServices/05-auth-service
gh secret set REDIS_URL -R GravityWavesGenerlServices/05-auth-service
gh secret set SECRET_KEY -R GravityWavesGenerlServices/05-auth-service
```

**Organization-level Secrets** (shared across all repos):

```powershell
# Go to: https://github.com/organizations/GravityWavesGenerlServices/settings/secrets/actions
# Add:
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - CODECOV_TOKEN
```

---

### 6. 📊 Monitoring & Observability

#### Setup Badges for README:

```markdown
<!-- CI Badge -->
[![CI](https://github.com/GravityWavesGenerlServices/05-auth-service/actions/workflows/ci.yml/badge.svg)](https://github.com/GravityWavesGenerlServices/05-auth-service/actions/workflows/ci.yml)

<!-- Coverage Badge -->
[![codecov](https://codecov.io/gh/GravityWavesGenerlServices/05-auth-service/branch/main/graph/badge.svg)](https://codecov.io/gh/GravityWavesGenerlServices/05-auth-service)

<!-- License Badge -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

---

### 7. 🔄 Clone Services for Development

#### Clone Single Service:

```powershell
# Clone specific service
gh repo clone GravityWavesGenerlServices/05-auth-service
cd 05-auth-service

# Install dependencies
pip install -e .

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Run locally
docker-compose up -d
uvicorn app.main:app --reload
```

#### Clone All Services:

```powershell
# Create workspace
mkdir E:\GravityServices
cd E:\GravityServices

# Clone all
$repos = gh repo list GravityWavesGenerlServices --limit 100 --json name -q '.[].name'
foreach ($repo in $repos) {
    Write-Host "Cloning $repo..."
    gh repo clone "GravityWavesGenerlServices/$repo"
}
```

---

### 8. 🧪 Testing the Setup

#### Test CI Workflow:

```powershell
# Make a small change
cd 05-auth-service
echo "# Test" >> README.md
git add README.md
git commit -m "test: trigger CI workflow"
git push

# Check workflow status
gh run list --repo GravityWavesGenerlServices/05-auth-service
```

#### Test Branch Protection:

```powershell
# Try to push directly to main (should fail)
git push origin main
# Error: protected branch

# Create PR instead (correct way)
git checkout -b feature/test-branch-protection
git push origin feature/test-branch-protection
gh pr create --title "Test: Branch Protection" --body "Testing branch protection rules"
```

---

### 9. 📱 Communication

#### Notify Team Members:

**Email Template**:
```
Subject: 🚀 Migration Complete - New Repository Structure

Hi Team,

Our microservices have been successfully migrated to a multi-repository architecture!

✅ What Changed:
- 52 independent repositories created
- Organization: https://github.com/GravityWavesGenerlServices
- Archive (old monorepo): https://github.com/Shakour-Data/GravityMicroServices-Archive

📋 Action Required:
1. Accept your GitHub organization invitation
2. Clone the services you're working on:
   gh repo clone GravityWavesGenerlServices/<service-name>

3. Review the documentation:
   - README in each repository
   - POST_MIGRATION_GUIDE.md

🔐 Security:
- All services now have CI/CD pipelines
- Branch protection enabled on main
- PR reviews required before merge

Questions? Reply to this email or check the documentation.

Best regards,
[Your Name]
```

---

### 10. 🎯 Best Practices Going Forward

#### Commit Guidelines:

```bash
# ✅ Good commit messages (English only!)
git commit -m "feat(auth): add OAuth2 support"
git commit -m "fix(database): resolve connection pool leak"
git commit -m "docs(readme): update installation guide"

# ❌ Bad commit messages
git commit -m "اضافه کردن ویژگی جدید"  # Not English!
git commit -m "fixed stuff"              # Too vague
git commit -m "WIP"                      # Not descriptive
```

#### PR Guidelines:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Coverage ≥ 80%

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

---

## 🆘 Troubleshooting

### Issue: "Repository not found"
**Solution**: Check organization access
```powershell
gh auth status
gh org list
```

### Issue: "Permission denied"
**Solution**: Request admin access
```powershell
# Owner needs to add you as org member
# Go to: https://github.com/orgs/GravityWavesGenerlServices/people
```

### Issue: "Workflow failed"
**Solution**: Check logs
```powershell
gh run list --repo GravityWavesGenerlServices/05-auth-service
gh run view <run-id> --log
```

### Issue: "Can't push to main"
**Solution**: This is correct! Create PR instead
```powershell
git checkout -b feature/my-feature
git push origin feature/my-feature
gh pr create
```

---

## 📞 Support

**Questions?**
- Documentation: Each repository's README.md
- Issues: Create issue in specific repository
- Discussions: https://github.com/orgs/GravityWavesGenerlServices/discussions

---

## ✅ Progress Tracking

- [x] Migration completed
- [x] Monorepo archived
- [ ] Branch protection configured
- [ ] CI/CD workflows added
- [ ] Team access configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] First PRs merged

---

**🎉 Happy Coding!** 🚀
