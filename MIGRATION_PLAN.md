# 🔧 Migration & Cleanup Strategy

> **Date:** November 10, 2025  
> **Purpose:** Clean integration of old services with new numbered structure

---

## 📊 Current Situation

### Old Services (Without Numbers):
```
api-gateway/              → Should map to: 03-api-gateway/
auth-service/             → Should map to: 05-auth-service/
common-library/           → Should map to: 01-common-library/
notification-service/     → Should map to: 07-notification-service/
service-discovery/        → Should map to: 02-service-discovery/
user-service/             → Should map to: 06-user-service/
```

### New Services (With Numbers):
```
01-common-library/        ✅ Created (empty structure)
02-service-discovery/     ✅ Created (empty structure)
03-api-gateway/           ✅ Created (empty structure)
05-auth-service/          ✅ Created (empty structure)
06-user-service/          ✅ Created (empty structure)
07-notification-service/  ✅ Created (empty structure)
+ 46 more new services (08-52)
```

---

## ✅ Recommended Strategy: MERGE OLD INTO NEW

### Step 1: Backup Old Services
```powershell
# Create backup directory
mkdir _OLD_SERVICES_BACKUP

# Move old services to backup
Move-Item api-gateway _OLD_SERVICES_BACKUP/
Move-Item auth-service _OLD_SERVICES_BACKUP/
Move-Item common-library _OLD_SERVICES_BACKUP/
Move-Item notification-service _OLD_SERVICES_BACKUP/
Move-Item service-discovery _OLD_SERVICES_BACKUP/
Move-Item user-service _OLD_SERVICES_BACKUP/
```

### Step 2: Migrate Code to Numbered Services

For each old service, copy working code to new numbered service:

#### Example: auth-service → 05-auth-service
```powershell
# Copy app code
Copy-Item -Recurse _OLD_SERVICES_BACKUP/auth-service/app/* 05-auth-service/app/ -Force

# Copy tests
Copy-Item -Recurse _OLD_SERVICES_BACKUP/auth-service/tests/* 05-auth-service/tests/ -Force

# Copy other important files
Copy-Item _OLD_SERVICES_BACKUP/auth-service/alembic.ini 05-auth-service/ -Force
Copy-Item _OLD_SERVICES_BACKUP/auth-service/pyproject.toml 05-auth-service/ -Force
Copy-Item _OLD_SERVICES_BACKUP/auth-service/.env.example 05-auth-service/ -Force

# Copy alembic versions
Copy-Item -Recurse _OLD_SERVICES_BACKUP/auth-service/alembic/versions/* 05-auth-service/alembic/versions/ -Force
```

### Step 3: Update References

After migration, update all internal references:
- Change `auth-service` → `05-auth-service` in configs
- Update import paths if needed
- Update .env files
- Update docker-compose if exists

---

## 🚀 Automated Migration Script

I'll create a PowerShell script to do this automatically!

---

## 📋 Migration Checklist

### Service: common-library → 01-common-library
- [ ] Backup old service
- [ ] Copy app/ code
- [ ] Copy tests/
- [ ] Copy pyproject.toml
- [ ] Update references
- [ ] Test migration
- [ ] Delete old after verification

### Service: service-discovery → 02-service-discovery
- [ ] Backup old service
- [ ] Copy app/ code
- [ ] Copy tests/
- [ ] Copy configuration
- [ ] Update references
- [ ] Test migration
- [ ] Delete old after verification

### Service: api-gateway → 03-api-gateway
- [ ] Backup old service
- [ ] Copy app/ code
- [ ] Copy tests/
- [ ] Copy middleware
- [ ] Update references
- [ ] Test migration
- [ ] Delete old after verification

### Service: auth-service → 05-auth-service
- [ ] Backup old service
- [ ] Copy app/ code
- [ ] Copy tests/
- [ ] Copy alembic migrations
- [ ] Update references
- [ ] Test migration
- [ ] Delete old after verification

### Service: user-service → 06-user-service
- [ ] Backup old service
- [ ] Copy app/ code
- [ ] Copy tests/
- [ ] Copy alembic migrations
- [ ] Update references
- [ ] Test migration
- [ ] Delete old after verification

### Service: notification-service → 07-notification-service
- [ ] Backup old service
- [ ] Copy app/ code (Phase 7 work!)
- [ ] Copy tests/
- [ ] Copy alembic migrations
- [ ] Update references
- [ ] Test migration
- [ ] Delete old after verification

---

## ⚠️ Important Notes

1. **Don't delete old services until migration is verified**
2. **Test each service after migration**
3. **Keep backup for at least 1 week**
4. **Update all documentation references**
5. **Notify all teams of new naming**

---

## 🎯 After Migration

### Clean Workspace:
```
✅ 01-common-library/       (with migrated code)
✅ 02-service-discovery/    (with migrated code)
✅ 03-api-gateway/          (with migrated code)
✅ 04-config-service/       (empty, ready for dev)
✅ 05-auth-service/         (with migrated code)
✅ 06-user-service/         (with migrated code)
✅ 07-notification-service/ (with migrated code + Phase 7)
✅ 08-52/                   (empty, ready for dev)
📁 _OLD_SERVICES_BACKUP/   (backup of old services)
```

### Update References:
- [ ] README.md - Already updated ✅
- [ ] SERVICES_INDEX.md - Already updated ✅
- [ ] TEAM_START_GUIDE.md - Already updated ✅
- [ ] docs/TEAM_DELEGATION_GUIDE.md
- [ ] All documentation files

---

**Next Step:** Create automated migration script!
