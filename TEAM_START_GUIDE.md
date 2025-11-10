# 🎯 دستورالعمل شروع کار تیم‌ها

> **تمام 52 سرویس با چهارچوب حرفه‌ای آماده است! ✅**

---

## ✅ وضعیت فعلی

### همین الان ساخته شد:
- ✅ **52 سرویس** با شماره‌گذاری استاندارد (`01` تا `52`)
- ✅ **ساختار حرفه‌ای** برای همه سرویس‌ها
- ✅ **آماده برای توسعه** - فوراً شروع کنید!

### لیست کامل سرویس‌ها:
```
P0 (هفته 1-2):   01-04   (4 سرویس)    🔴 اولویت بالا
P1 (هفته 3-8):   05-14   (10 سرویس)   🟠 اولویت متوسط-بالا
P2 (هفته 9-16):  15-27   (13 سرویس)   🟡 اولویت متوسط
P3 (هفته 17-24): 28-37   (10 سرویس)   🟢 اولویت متوسط-پایین
P4 (هفته 25-30): 38-52   (15 سرویس)   🔵 اولویت پایین
```

---

## 📋 دستورالعمل برای هر تیم

### Team 1: Core Infrastructure
**سرویس‌های شما:**
- `01-common-library` (پایه - شروع از اینجا)
- `04-config-service`

**دستور شروع:**
```powershell
cd 01-common-library
# شروع توسعه
```

---

### Team 2: DevOps & Monitoring
**سرویس‌های شما:**
- `02-service-discovery`
- `14-cache-service`
- `38-monitoring-service`
- `39-logging-service`
- `44-backup-service`

**دستور شروع:**
```powershell
cd 02-service-discovery
python -m uvicorn app.main:app --port 8500 --reload
```

---

### Team 3: Backend Infrastructure
**سرویس شما:**
- `03-api-gateway`

**دستور شروع:**
```powershell
cd 03-api-gateway
python -m uvicorn app.main:app --port 8000 --reload
```

---

### Team 4: Security & Authentication
**سرویس‌های شما:**
- `05-auth-service`
- `11-permission-service`
- `12-session-service`
- `13-audit-log-service`
- `45-rate-limiter-service`
- `50-kyc-service`

**دستور شروع:**
```powershell
cd 05-auth-service
python -m uvicorn app.main:app --port 8081 --reload
```

---

### Team 5: Backend A - User & Notifications
**سرویس‌های شما:**
- `06-user-service`
- `07-notification-service`

**دستور شروع:**
```powershell
cd 06-user-service
python -m uvicorn app.main:app --port 8082 --reload
```

---

### Team 6: Backend B - Communication
**سرویس‌های شما:**
- `08-email-service`
- `09-sms-service`
- `10-file-storage-service`

**دستور شروع:**
```powershell
cd 08-email-service
python -m uvicorn app.main:app --port 8086 --reload
```

---

### Team 7: FinTech
**سرویس‌های شما:**
- `15-payment-service` 💰
- `27-invoice-service`
- `31-subscription-service`
- `48-tax-service`

**دستور شروع:**
```powershell
cd 15-payment-service
python -m uvicorn app.main:app --port 8100 --reload
```

---

### Team 8: Backend C/D - E-commerce
**سرویس‌های شما:**
- `16-order-service`
- `17-product-service`
- `18-cart-service`
- `25-inventory-service`

**دستور شروع:**
```powershell
cd 16-order-service
python -m uvicorn app.main:app --port 8101 --reload
```

---

### Team 9: Backend E/F - Features
**سرویس‌های شما:**
- `21-review-service`
- `22-wishlist-service`
- `24-reporting-service`
- `26-shipping-service`
- `33-coupon-service`
- `37-feedback-service`

**دستور شروع:**
```powershell
cd 21-review-service
python -m uvicorn app.main:app --port 8106 --reload
```

---

### Team 10: Search & Analytics
**سرویس‌های شما:**
- `19-search-service` 🔍
- `20-recommendation-service`
- `23-analytics-service`

**دستور شروع:**
```powershell
cd 19-search-service
python -m uvicorn app.main:app --port 8104 --reload
```

---

### Team 11: Real-Time Services
**سرویس‌های شما:**
- `28-chat-service` 💬
- `29-video-call-service` 📹
- `30-geolocation-service` 📍

**دستور شروع:**
```powershell
cd 28-chat-service
python -m uvicorn app.main:app --port 8120 --reload
```

---

### Team 12: Specialized Features
**سرویس‌های شما:**
- `32-loyalty-service`
- `34-referral-service`
- `35-translation-service`
- `36-cms-service`
- `40-scheduler-service`
- `41-webhook-service`
- `42-export-service`
- `43-import-service`
- `46-ab-testing-service`
- `47-feature-flag-service`
- `49-fraud-detection-service`
- `51-gamification-service`
- `52-social-media-service`

**دستور شروع:**
```powershell
cd 32-loyalty-service
python -m uvicorn app.main:app --port 8124 --reload
```

---

## 🚀 مراحل شروع کار (برای همه تیم‌ها)

### مرحله 1: ورود به سرویس
```powershell
cd ##-service-name
```

### مرحله 2: بررسی ساختار
```powershell
ls
# شما باید ببینید:
# - app/          (کد اصلی)
# - tests/        (تست‌ها)
# - README.md     (مستندات)
# - .env.example  (تنظیمات نمونه)
```

### مرحله 3: بررسی README
```powershell
notepad README.md
# اطلاعات مهم:
# - شماره پورت سرویس
# - نوع دیتابیس
# - دستورات اجرا
```

### مرحله 4: ایجاد .env
```powershell
Copy-Item .env.example .env
notepad .env
# تنظیمات را ویرایش کنید
```

### مرحله 5: اجرای سرویس
```powershell
python -m uvicorn app.main:app --port #### --reload
# #### = شماره پورت سرویس شما
```

### مرحله 6: تست Health Check
مرورگر را باز کنید:
```
http://localhost:####/health
```

باید پاسخ دریافت کنید:
```json
{
  "status": "healthy",
  "service": "##-service-name"
}
```

### مرحله 7: بررسی API Docs
```
http://localhost:####/docs
```

---

## 📁 ساختار هر سرویس (یکسان برای همه)

```
##-service-name/
├── app/
│   ├── main.py          ✅ آماده - FastAPI app
│   ├── config.py        ✅ آماده - تنظیمات
│   ├── api/v1/          📝 شما: API endpoints
│   ├── services/        📝 شما: Business logic
│   ├── models/          📝 شما: Database models
│   └── schemas/         📝 شما: Pydantic schemas
├── tests/               📝 شما: تست‌ها (95%+ coverage)
├── README.md            ✅ آماده - مستندات
├── .env.example         ✅ آماده - نمونه تنظیمات
└── .gitignore           ✅ آماده
```

**✅ آماده** = قبلاً ساخته شده، می‌توانید استفاده کنید  
**📝 شما** = باید توسط تیم پیاده‌سازی شود

---

## 🎯 اولویت کاری

### هفته 1-2: P0 (شروع فوری! 🔴)
**تیم‌های فعال:** 1, 2, 3
```
01-common-library         (Team 1) - بالاترین اولویت
02-service-discovery      (Team 2)
03-api-gateway           (Team 3)
04-config-service        (Team 1)
```

### هفته 3-8: P1 (بعد از P0 ✅)
**تیم‌های فعال:** 4, 5, 6, 2
```
05-auth-service          (Team 4)
06-user-service          (Team 5)
07-notification-service  (Team 5)
08-email-service         (Team 6)
09-sms-service           (Team 6)
10-file-storage-service  (Team 6)
11-permission-service    (Team 4)
12-session-service       (Team 4)
13-audit-log-service     (Team 4)
14-cache-service         (Team 2)
```

### هفته 9-16: P2 (بعد از P1 ✅)
**تیم‌های فعال:** 7, 8, 9, 10
```
15-27: Business services
```

### هفته 17-24: P3
**تیم‌های فعال:** 11, 12, 7, 9
```
28-37: Advanced features
```

### هفته 25-30: P4
**تیم‌های فعال:** 2, 4, 7, 12
```
38-52: Specialized services
```

---

## ✅ چک‌لیست توسعه (برای هر سرویس)

- [ ] ✅ سرویس اجرا می‌شود (`/health` پاسخ می‌دهد)
- [ ] 📝 API endpoints نوشته شده‌اند
- [ ] 📝 Business logic پیاده‌سازی شده
- [ ] 📝 Database models ایجاد شده‌اند
- [ ] 📝 Tests نوشته شده (95%+ coverage)
- [ ] 📝 Documentation کامل است
- [ ] 🐳 Docker image می‌سازد
- [ ] 🚀 Production ready

---

## 📊 پیگیری پیشرفت

### هر هفته گزارش دهید:

**فرمت گزارش:**
```
تیم: Team #
سرویس: ##-service-name
وضعیت: 🔄 در حال توسعه
پیشرفت: ##%

انجام شده این هفته:
- ✅ مورد 1
- ✅ مورد 2

برنامه هفته آینده:
- ⏳ مورد 1
- ⏳ مورد 2

مشکلات:
- مشکل 1 (در صورت وجود)
```

---

## 🆘 پشتیبانی

### مستندات:
- **Index کامل:** `SERVICES_INDEX.md`
- **راهنمای تیم‌ها:** `docs/TEAM_DELEGATION_GUIDE.md`
- **لیست سرویس‌ها:** `docs/NUMBERED_SERVICES_LIST.md`
- **راهنمای فارسی:** `docs/QUICK_START_FA.md`

### دستورات مفید:
```powershell
# دیدن همه سرویس‌ها
Get-ChildItem -Directory -Filter "*-*" | Sort-Object Name

# شمارش سرویس‌ها
(Get-ChildItem -Directory -Filter "*-*").Count

# پیدا کردن سرویس خاص
Get-ChildItem -Directory -Filter "*payment*"
```

---

## 🎉 آماده برای شروع!

**همه چیز آماده است:**
- ✅ 52 سرویس با ساختار حرفه‌ای
- ✅ شماره‌گذاری استاندارد (01-52)
- ✅ اولویت‌بندی واضح (P0-P4)
- ✅ تخصیص تیمی مشخص
- ✅ مستندات کامل

**اکنون شروع کنید! 🚀**

---

**تاریخ ایجاد:** 10 نوامبر 2025  
**وضعیت:** ✅ همه سرویس‌ها آماده  
**تیم‌ها:** 12 تیم تخصصی  
**سرویس‌ها:** 52 میکروسرویس
