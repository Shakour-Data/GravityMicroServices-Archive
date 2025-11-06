# 🏗️ معماری مستقل میکروسرویس‌ها - Independent Microservices Architecture

## 📋 اصول طراحی

### استقلال کامل (100% Independence)
هر میکروسرویس باید:
1. ✅ **Git Repository مجزا** داشته باشد
2. ✅ **Virtual Environment خودش** (.venv)
3. ✅ **Docker Compose خودش** برای دیتابیس و سرویس‌های وابسته
4. ✅ **Database اختصاصی** (PostgreSQL instance خودش)
5. ✅ **Dependencies مجزا** (pyproject.toml خودش)
6. ✅ **CI/CD Pipeline خودش** (GitHub Actions / GitLab CI)
7. ✅ **Documentation خودش** (README, API docs)
8. ✅ **قابلیت اجرای مستقل** بدون نیاز به سرویس‌های دیگر

---

## 🗂️ ساختار جدید پروژه

به جای یک **Monorepo**، خواهیم داشت:

```
gravity-microservices/
├── gravity-infrastructure/          # Repository 1 - Shared Infrastructure
│   ├── docker-compose.yml           # All shared services (optional)
│   ├── kubernetes/                  # K8s manifests
│   ├── monitoring/                  # Prometheus, Grafana configs
│   └── README.md
│
├── gravity-common/                  # Repository 2 - Shared Library (PyPI package)
│   ├── gravity_common/
│   ├── pyproject.toml
│   ├── .git/
│   └── README.md
│
├── auth-service/                    # Repository 3 - Auth Service
│   ├── app/
│   ├── tests/
│   ├── docker-compose.yml           # PostgreSQL + Redis for auth
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── .git/
│   ├── .venv/                       # Virtual environment
│   └── README.md
│
├── api-gateway/                     # Repository 4 - API Gateway
│   ├── app/
│   ├── docker-compose.yml           # Gateway dependencies
│   ├── .git/
│   ├── .venv/
│   └── ...
│
├── user-service/                    # Repository 5 - User Service
│   ├── app/
│   ├── docker-compose.yml           # PostgreSQL for users
│   ├── .git/
│   ├── .venv/
│   └── ...
│
├── notification-service/            # Repository 6 - Notification Service
│   ├── app/
│   ├── docker-compose.yml           # PostgreSQL + RabbitMQ
│   ├── .git/
│   ├── .venv/
│   └── ...
│
├── file-storage-service/            # Repository 7 - File Storage
│   ├── app/
│   ├── docker-compose.yml           # PostgreSQL + MinIO
│   ├── .git/
│   ├── .venv/
│   └── ...
│
└── payment-service/                 # Repository 8 - Payment Service
    ├── app/
    ├── docker-compose.yml           # PostgreSQL for payments
    ├── .git/
    ├── .venv/
    └── ...
```

---

## 📦 هر Repository شامل:

### 1. Git Repository (مستقل)
```bash
cd auth-service
git init
git remote add origin https://github.com/gravity/auth-service.git
```

### 2. Virtual Environment (مستقل)
```bash
cd auth-service
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
poetry install
```

### 3. Docker Compose (مستقل)
```yaml
# auth-service/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: auth_db
      POSTGRES_USER: auth_user
      POSTGRES_PASSWORD: auth_pass
    ports:
      - "5432:5432"
    volumes:
      - auth_postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - auth_redis_data:/data
  
  auth-service:
    build: .
    ports:
      - "8001:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql+asyncpg://auth_user:auth_pass@postgres:5432/auth_db
      REDIS_URL: redis://redis:6379/0

volumes:
  auth_postgres_data:
  auth_redis_data:
```

### 4. Dependencies (مستقل)
```toml
# auth-service/pyproject.toml
[tool.poetry]
name = "auth-service"
version = "1.0.0"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.1"
sqlalchemy = "^2.0.23"
asyncpg = "^0.29.0"
# gravity-common from PyPI or Git
gravity-common = {git = "https://github.com/gravity/gravity-common.git", tag = "v1.0.0"}
```

### 5. Dockerfile (مستقل)
هر سرویس Dockerfile خودش را دارد

### 6. CI/CD Pipeline (مستقل)
```yaml
# auth-service/.github/workflows/ci.yml
name: Auth Service CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          poetry install
          poetry run pytest
```

---

## 🔗 نحوه استفاده از Common Library

### گزینه 1: انتشار در PyPI (توصیه می‌شود)
```bash
# در gravity-common repository
poetry build
poetry publish

# در سرویس‌ها
# pyproject.toml
[tool.poetry.dependencies]
gravity-common = "^1.0.0"
```

### گزینه 2: نصب از Git
```bash
# در سرویس‌ها
# pyproject.toml
[tool.poetry.dependencies]
gravity-common = {git = "https://github.com/gravity/gravity-common.git", tag = "v1.0.0"}
```

### گزینه 3: نصب از مسیر محلی (فقط Development)
```bash
# pyproject.toml
[tool.poetry.dependencies]
gravity-common = {path = "../gravity-common", develop = true}
```

---

## 🚀 راه‌اندازی هر سرویس (مستقل)

### مثال: Auth Service

```bash
# 1. Clone repository
git clone https://github.com/gravity/auth-service.git
cd auth-service

# 2. ایجاد virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. نصب dependencies
poetry install

# 4. راه‌اندازی infrastructure (PostgreSQL + Redis)
docker-compose up -d postgres redis

# 5. اجرای migrations
poetry run alembic upgrade head

# 6. ایجاد superuser
poetry run python scripts/create_superuser.py

# 7. اجرای سرویس
poetry run uvicorn app.main:create_app --factory --reload

# سرویس در http://localhost:8001 در دسترس است
```

**هیچ وابستگی به سرویس دیگری ندارد!** ✅

---

## 🌐 ارتباط بین سرویس‌ها

### در محیط Development (Local):
```yaml
# هر سرویس می‌تواند مستقل اجرا شود
# اگر نیاز به ارتباط بود، از HTTP APIs استفاده می‌شود

# مثال: User Service نیاز به Auth دارد
# user-service/.env
AUTH_SERVICE_URL=http://localhost:8001
```

### در محیط Production (Kubernetes):
```yaml
# استفاده از Service Discovery (Consul/Kubernetes DNS)
# هر سرویس با نام DNS دیگری صدا می‌زند

# مثال:
AUTH_SERVICE_URL=http://auth-service.gravity-services.svc.cluster.local:8000
```

---

## 📊 مزایای این معماری

### ✅ استقلال کامل
- هر تیم می‌تواند روی سرویس خودش کار کند
- هیچ conflict در Git نداریم
- هر سرویس با سرعت خودش توسعه می‌یابد

### ✅ Scalability
- هر سرویس به‌طور مستقل scale می‌شود
- منابع به‌طور مستقل تخصیص داده می‌شوند
- Database هر سرویس جداست (no bottleneck)

### ✅ Deployment مستقل
- Deploy هر سرویس بدون تأثیر روی بقیه
- Rollback آسان
- CI/CD مستقل برای هر سرویس

### ✅ Technology Freedom
- هر سرویس می‌تواند از تکنولوژی متفاوتی استفاده کند
- آزادی در انتخاب database
- آزادی در انتخاب framework

### ✅ Fault Isolation
- خرابی یک سرویس به بقیه سرایت نمی‌کند
- Circuit breaker برای حفاظت
- Graceful degradation

---

## 🎯 ساختار استاندارد هر Repository

```
service-name/
├── .git/                           # Git repository
├── .venv/                          # Virtual environment (gitignored)
├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI pipeline
│       └── cd.yml                  # CD pipeline
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── api/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── alembic/
│   ├── versions/
│   └── env.py
├── scripts/
│   └── *.py
├── kubernetes/
│   ├── deployment.yml
│   ├── service.yml
│   └── ingress.yml
├── docker-compose.yml              # Infrastructure for this service
├── Dockerfile                      # Multi-stage build
├── pyproject.toml                  # Poetry dependencies
├── poetry.lock                     # Locked dependencies
├── alembic.ini                     # Alembic config
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore
├── README.md                       # Service documentation
├── DEPLOYMENT.md                   # Deployment guide
└── LICENSE                         # License file
```

---

## 🔧 Infrastructure Repository

Repository مجزا برای:
- Docker Compose با تمام سرویس‌های مشترک (اختیاری)
- Kubernetes manifests
- Monitoring configs (Prometheus, Grafana)
- Logging configs (ELK)
- Tracing configs (Jaeger)

```bash
# gravity-infrastructure/
├── docker-compose.full.yml         # همه سرویس‌ها (برای Development)
├── kubernetes/
│   ├── namespaces/
│   ├── auth-service/
│   ├── user-service/
│   └── ...
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── alertmanager/
└── logging/
    ├── elasticsearch/
    ├── logstash/
    └── kibana/
```

---

## 📝 Common Library به عنوان Package

```bash
# gravity-common repository
gravity-common/
├── .git/
├── gravity_common/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── models.py
│   ├── security.py
│   ├── database.py
│   ├── redis_client.py
│   ├── logging_config.py
│   └── utils.py
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE

# انتشار در PyPI
poetry build
poetry publish

# یا استفاده از Git tag
git tag v1.0.0
git push origin v1.0.0
```

---

## 🎯 Development Workflow

### برای هر توسعه‌دهنده:

```bash
# 1. Clone سرویس مورد نظر
git clone https://github.com/gravity/auth-service.git
cd auth-service

# 2. Setup environment
python -m venv .venv
source .venv/bin/activate
poetry install

# 3. راه‌اندازی dependencies
docker-compose up -d

# 4. کار روی feature
git checkout -b feature/new-feature
# ... کدنویسی ...

# 5. Test
poetry run pytest

# 6. Commit & Push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 7. Pull Request
# ایجاد PR در GitHub/GitLab
```

---

## 🚀 مراحل بعدی

### فاز 1: بازسازی ساختار
1. ✅ جداسازی auth-service به repository مستقل
2. ✅ ایجاد gravity-common package
3. ✅ ایجاد infrastructure repository
4. ✅ تست استقلال کامل

### فاز 2: توسعه سرویس‌های جدید
هر سرویس جدید:
1. ایجاد repository مجزا
2. استفاده از template استاندارد
3. Docker Compose مستقل
4. CI/CD Pipeline
5. Documentation کامل

---

## 📊 مقایسه: قبل و بعد

### ❌ قبل (Monorepo):
```
gravity-microservices/
├── common-library/
├── auth-service/
├── user-service/
└── ...

مشکلات:
- یک Git repo برای همه
- Conflict در merge
- Deploy همه با هم
- وابستگی‌های مشترک
```

### ✅ بعد (Independent Repos):
```
GitHub/GitLab Organization: gravity/
├── gravity-common          (Package)
├── gravity-infrastructure  (Configs)
├── auth-service           (Independent)
├── user-service           (Independent)
└── ...

مزایا:
- هر repo مستقل
- No conflicts
- Deploy مستقل
- Technology freedom
```

---

## 🎉 نتیجه

با این معماری:
1. ✅ هر سرویس **کاملاً مستقل** است
2. ✅ می‌توان در **پروژه‌های نامحدود** استفاده کرد
3. ✅ هر تیم **مستقل** کار می‌کند
4. ✅ **Scalability** بالا
5. ✅ **Maintainability** بهتر
6. ✅ **CI/CD** مستقل
7. ✅ **No conflicts** در Git
8. ✅ **Production-ready** architecture

---

**این معماری واقعی Enterprise است! 🚀**
