# 🧹 راهنمای تمیز کردن Monorepo بعد از Migration

## ✅ وضعیت فعلی
- همه 52 سرویس به Organization جدید منتقل شدند
- Monorepo محلی هنوز 225 تغییر uncommitted دارد
- این تغییرات عمدتاً از تغییر نام پوشه‌ها هستند

---

## 🎯 گزینه 1: Archive کردن Monorepo (توصیه می‌شود)

### مرحله 1: Commit تغییرات به عنوان "Migration Complete"
```bash
cd E:\Shakour\GravityMicroServices
git add .
git commit -m "🚀 Migration Complete: All services moved to separate repositories

- Migrated 52 services to GravityWavesGenerlServices organization
- Each service now has its own repository with full Git history
- This monorepo is now archived for reference only
- New development should happen in individual service repositories

Organization: https://github.com/GravityWavesGenerlServices"
```

### مرحله 2: Push به GitHub
```bash
git push origin main
```

### مرحله 3: Archive کردن Repository در GitHub
1. برو به: https://github.com/GravityWavesMl/GravityMicroServices/settings
2. پایین صفحه بخش "Danger Zone"
3. کلیک روی "Archive this repository"
4. تایید کن

### مرحله 4: اضافه کردن README توضیحات
در README.md این متن را اضافه کن:

```markdown
# ⚠️ این Repository به Archive منتقل شده است

این پروژه به معماری Multi-repo مهاجرت کرده است.

## 🔗 Repository های جدید:
همه سرویس‌ها اکنون در Organization جداگانه هستند:
👉 https://github.com/GravityWavesGenerlServices

## 📦 52 Repository جدید:
- [01-common-library](https://github.com/GravityWavesGenerlServices/01-common-library)
- [02-service-discovery](https://github.com/GravityWavesGenerlServices/02-service-discovery)
- [03-api-gateway](https://github.com/GravityWavesGenerlServices/03-api-gateway)
- ... و 49 سرویس دیگر

## 📅 تاریخ Migration: 10 نوامبر 2025

برای توسعه جدید، لطفاً به repository های جداگانه مراجعه کنید.
```

---

## 🎯 گزینه 2: Reset کردن به قبل از تغییرات

اگر می‌خواهی تغییرات را نگه نداری:

```bash
cd E:\Shakour\GravityMicroServices
git reset --hard HEAD
git clean -fd
```

⚠️ **هشدار**: این کار همه تغییرات uncommitted را حذف می‌کند!

---

## 🎯 گزینه 3: حذف کامل Monorepo محلی

اگر دیگر به Monorepo نیازی نداری:

```bash
# فقط پوشه محلی را حذف کن (repository GitHub دست نخورده می‌ماند)
cd E:\Shakour
Remove-Item -Recurse -Force GravityMicroServices
```

---

## 📁 نحوه کار با Repository های جدید

### Clone کردن یک سرویس خاص:
```bash
# مثال: Service Discovery
git clone https://github.com/GravityWavesGenerlServices/02-service-discovery.git

# مثال: Auth Service
git clone https://github.com/GravityWavesGenerlServices/05-auth-service.git
```

### Clone کردن همه (اختیاری):
```bash
# ساخت پوشه جدید برای همه سرویس‌ها
mkdir E:\Shakour\GravityServices
cd E:\Shakour\GravityServices

# Clone کردن همه 52 repository
# (می‌توانید اسکریپت بنویسید یا دستی clone کنید)
gh repo list GravityWavesGenerlServices --limit 100 --json name -q '.[].name' | ForEach-Object {
    gh repo clone "GravityWavesGenerlServices/$_"
}
```

---

## ✅ Checklist تمام شدن Migration:

- [ ] Commit تغییرات Monorepo
- [ ] Push به GitHub
- [ ] Update کردن README.md با لینک‌های جدید
- [ ] Archive کردن Monorepo در GitHub
- [ ] Clone کردن سرویس‌هایی که روی آن‌ها کار می‌کنید
- [ ] تنظیم CI/CD برای repository های جدید
- [ ] اطلاع‌رسانی به تیم درباره آدرس‌های جدید

---

## 🆘 اگر مشکلی پیش آمد:

Monorepo هنوز روی GitHub هست و می‌توانید به آن برگردید:
```bash
git clone https://github.com/GravityWavesMl/GravityMicroServices.git
```

همه سرویس‌ها هم در Organization جدید با تاریخچه کامل Git موجودند.
