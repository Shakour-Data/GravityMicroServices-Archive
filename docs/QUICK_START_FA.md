# 🎯 چگونه تیم خود را راه‌اندازی کنم؟ (راهنمای سریع برای تیم‌لیدرها)

این راهنما به زبان فارسی برای تیم‌لیدرهایی است که می‌خواهند سرویس‌های خود را شروع کنند.

---

## 📋 مرحله 1: شناسایی سرویس‌های تیم شما

**فایل مرجع:** `docs/TEAM_DELEGATION_GUIDE.md`

### تیم‌ها و سرویس‌های اختصاص داده شده:

| تیم | سرویس‌ها | تعداد |
|-----|----------|-------|
| **Team 1: Core Infrastructure** | 01, 04 | 2 سرویس |
| **Team 2: DevOps** | 02, 14, 38, 39, 44 | 5 سرویس |
| **Team 3: Backend Infrastructure** | 03 | 1 سرویس |
| **Team 4: Security** | 05, 11, 12, 13, 45, 50 | 6 سرویس |
| **Team 5: Backend A** | 06, 07 | 2 سرویس |
| **Team 6: Backend B** | 08, 09, 10 | 3 سرویس |
| **Team 7: FinTech** | 15, 27, 31, 48 | 4 سرویس |
| **Team 8: Backend C/D** | 16, 17, 18, 25 | 4 سرویس |
| **Team 9: Backend E/F** | 21, 22, 24, 26, 33, 37 | 6 سرویس |
| **Team 10: Search & Analytics** | 19, 20, 23 | 3 سرویس |
| **Team 11: Real-Time** | 28, 29, 30 | 3 سرویس |
| **Team 12: Specialized** | 32, 34, 35, 36, 40-43, 46, 47, 49, 51, 52 | 13 سرویس |

---

## 🚀 مرحله 2: ایجاد سرویس‌های خود

### گزینه A: ایجاد تک‌به‌تک (توصیه می‌شود)

```powershell
# مثال: Team 6 می‌خواهد سرویس 08 را ایجاد کند
cd E:\Shakour\GravityMicroServices
.\scripts\Initialize-AllServices.ps1 -StartFrom 8 -EndAt 8
```

### گزینه B: ایجاد همه سرویس‌های تیم به یکباره

```powershell
# مثال: Team 6 سرویس‌های 08, 09, 10 را می‌خواهد
cd E:\Shakour\GravityMicroServices

# سرویس 08
.\scripts\Initialize-AllServices.ps1 -StartFrom 8 -EndAt 8

# سرویس 09
.\scripts\Initialize-AllServices.ps1 -StartFrom 9 -EndAt 9

# سرویس 10
.\scripts\Initialize-AllServices.ps1 -StartFrom 10 -EndAt 10
```

### گزینه C: ایجاد محدوده سرویس‌ها

```powershell
# ایجاد سرویس‌های 15 تا 18
.\scripts\Initialize-AllServices.ps1 -StartFrom 15 -EndAt 18
```

---

## 📂 مرحله 3: ساختار سرویس ایجاد شده

بعد از اجرای اسکریپت، هر سرویس این ساختار را دارد:

```
##-service-name/
├── app/
│   ├── main.py          ✅ آماده برای اجرا
│   ├── config.py        ✅ تنظیمات پایه
│   ├── api/v1/          📝 API endpoints اینجا
│   ├── services/        📝 Business logic اینجا
│   ├── models/          📝 Database models اینجا
│   └── schemas/         📝 Pydantic schemas اینجا
├── tests/               📝 تست‌ها اینجا
├── .env.example         ✅ نمونه تنظیمات
├── README.md            ✅ مستندات
└── .gitignore           ✅ Git ignore
```

---

## 🔧 مرحله 4: راه‌اندازی سرویس

### 4.1. ورود به پوشه سرویس

```powershell
cd 08-email-service
```

### 4.2. ایجاد فایل .env

```powershell
# کپی از نمونه
Copy-Item .env.example .env

# ویرایش فایل .env با تنظیمات واقعی
notepad .env
```

### 4.3. نصب dependencies (اختیاری - اگر Poetry دارید)

```powershell
poetry install
```

### 4.4. اجرای سرویس

```powershell
# با Poetry
poetry run uvicorn app.main:app --port 8086 --reload

# یا بدون Poetry
python -m uvicorn app.main:app --port 8086 --reload
```

### 4.5. بررسی سلامت سرویس

مرورگر خود را باز کنید:
- **Health Check:** http://localhost:8086/health
- **API Docs:** http://localhost:8086/docs
- **ReDoc:** http://localhost:8086/redoc

---

## 📝 مرحله 5: شروع توسعه

### 5.1. بررسی مستندات سرویس

```powershell
# باز کردن README سرویس
notepad README.md
```

### 5.2. بررسی لیست کامل سرویس‌ها

```powershell
# باز کردن لیست شماره‌گذاری شده
notepad ..\docs\NUMBERED_SERVICES_LIST.md
```

### 5.3. بررسی راهنمای تیم

```powershell
# باز کردن راهنمای تخصیص تیم‌ها
notepad ..\docs\TEAM_DELEGATION_GUIDE.md
```

---

## 🎯 مرحله 6: چک‌لیست توسعه

برای هر سرویس، اطمینان حاصل کنید:

- [ ] ✅ سرویس اجرا می‌شود (Health check پاسخ می‌دهد)
- [ ] ✅ Database متصل است
- [ ] ✅ Redis (در صورت نیاز) کار می‌کند
- [ ] 📝 API endpoints نوشته شده‌اند
- [ ] 📝 Business logic پیاده‌سازی شده
- [ ] 📝 Tests نوشته شده (95%+ coverage)
- [ ] 📝 Documentation کامل است
- [ ] 🐳 Docker image می‌سازد
- [ ] 🚀 Ready for deployment

---

## 📊 مرحله 7: گزارش پیشرفت

### هفتگی به تیم‌لید اصلی گزارش دهید:

```
Service: 08-email-service
Status: 🔄 50% Complete
Completed:
  ✅ Basic structure
  ✅ Health check endpoint
  ✅ Database connection
  ✅ SMTP integration
In Progress:
  🔄 Template rendering
  🔄 Email queue
Not Started:
  ⏳ Bounce handling
  ⏳ Analytics
```

---

## 🆘 مشکل دارید؟

### مشکلات رایج:

**1. اسکریپت اجرا نمی‌شود:**
```powershell
# اجازه اجرا دهید
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**2. Port قبلاً استفاده می‌شود:**
```powershell
# پورت دیگری استفاده کنید
uvicorn app.main:app --port 8087 --reload
```

**3. Database متصل نمی‌شود:**
- بررسی کنید PostgreSQL نصب است؟
- `.env` فایل را با تنظیمات صحیح پر کنید

**4. Import error:**
```powershell
# مطمئن شوید در پوشه درست هستید
cd 08-email-service
python -m uvicorn app.main:app --reload
```

---

## 📚 منابع اضافی

| فایل | موضوع |
|------|-------|
| `docs/NUMBERED_SERVICES_LIST.md` | لیست کامل 52 سرویس با شماره‌گذاری |
| `docs/TEAM_DELEGATION_GUIDE.md` | تخصیص سرویس‌ها به تیم‌ها |
| `docs/MICROSERVICES_ARCHITECTURE.md` | معماری کامل پلتفرم |
| `docs/service-templates/` | Template فایل‌ها |
| `scripts/Initialize-AllServices.ps1` | اسکریپت ایجاد سرویس |

---

## ✅ مثال کامل: Team 7 (FinTech)

```powershell
# 1. ورود به پروژه
cd E:\Shakour\GravityMicroServices

# 2. ایجاد سرویس 15 (payment-service)
.\scripts\Initialize-AllServices.ps1 -StartFrom 15 -EndAt 15

# 3. ورود به سرویس
cd 15-payment-service

# 4. کپی تنظیمات
Copy-Item .env.example .env

# 5. اجرا
python -m uvicorn app.main:app --port 8100 --reload

# 6. تست در مرورگر
# http://localhost:8100/health
# http://localhost:8100/docs

# 7. شروع توسعه!
code .  # باز کردن در VS Code
```

---

## 🎉 موفق باشید!

حالا تیم شما آماده است تا روی سرویس‌های اختصاص داده شده کار کند!

**سؤال دارید؟** به `TEAM_DELEGATION_GUIDE.md` مراجعه کنید یا با تیم‌لید اصلی تماس بگیرید.

---

**تاریخ ایجاد:** 10 نوامبر 2025  
**نسخه:** 1.0.0  
**زبان:** فارسی 🇮🇷
