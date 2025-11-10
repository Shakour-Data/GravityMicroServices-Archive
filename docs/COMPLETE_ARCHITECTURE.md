# 🏗️ GRAVITY MICROSERVICES - COMPLETE ARCHITECTURE

> **Complete architectural framework for all 52 independent microservices**

**Version:** 1.0.0  
**Last Updated:** November 10, 2025  
**Status:** Production Ready

---

## 📑 TABLE OF CONTENTS

1. [Architecture Overview](#architecture-overview)
2. [Service Categories](#service-categories)
3. [Common Architecture Patterns](#common-architecture-patterns)
4. [Service-Specific Architectures](#service-specific-architectures)
5. [Communication Patterns](#communication-patterns)
6. [Data Management Strategy](#data-management-strategy)
7. [Security Architecture](#security-architecture)
8. [Deployment Architecture](#deployment-architecture)
9. [Monitoring & Observability](#monitoring--observability)

---

## 🎯 ARCHITECTURE OVERVIEW

### Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURAL PRINCIPLES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  100% INDEPENDENCE                                          │
│     • Each service is completely autonomous                     │
│     • No direct dependencies between services                   │
│     • Can be deployed, scaled, and maintained independently     │
│                                                                 │
│  2️⃣  DATABASE PER SERVICE                                        │
│     • Each service owns its data                                │
│     • No shared databases                                       │
│     • Data sharing only through APIs                            │
│                                                                 │
│  3️⃣  API-FIRST DESIGN                                            │
│     • RESTful APIs for synchronous communication                │
│     • Event-driven for asynchronous operations                  │
│     • GraphQL for complex data queries (optional)               │
│                                                                 │
│  4️⃣  POLYGLOT PERSISTENCE                                        │
│     • PostgreSQL for relational data                            │
│     • Redis for caching and pub/sub                             │
│     • Elasticsearch for search (where needed)                   │
│     • MongoDB for document storage (where needed)               │
│                                                                 │
│  5️⃣  CLOUD-NATIVE READY                                          │
│     • Containerized with Docker                                 │
│     • Kubernetes manifests included                             │
│     • Horizontal scaling support                                │
│     • Health checks and readiness probes                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATIONS                              │
│              (Web, Mobile, Desktop, Third-party Apps)                    │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    03-API-GATEWAY (Port 8000)                            │
│  • Authentication & Authorization                                        │
│  • Rate Limiting & Circuit Breaking                                      │
│  • Request Routing & Load Balancing                                      │
│  • API Composition & Transformation                                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 02-SERVICE-DISCOVERY (Port 8761)                         │
│  • Service Registration                                                  │
│  • Health Monitoring                                                     │
│  • Dynamic Service Discovery                                             │
└─────────────────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ CORE         │    │ BUSINESS     │    │ SUPPORT      │
│ SERVICES     │    │ SERVICES     │    │ SERVICES     │
│ (P0 + P1)    │    │ (P2)         │    │ (P3 + P4)    │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    MESSAGE BROKER & EVENT BUS                            │
│  • RabbitMQ: Task queues, work distribution                              │
│  • Apache Kafka: Event streaming, event sourcing                         │
│  • Redis Pub/Sub: Real-time notifications                                │
└─────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DATA LAYER (Per Service)                              │
│  • PostgreSQL: Primary relational database                               │
│  • Redis: Caching + Session storage                                      │
│  • Elasticsearch: Search & analytics (optional)                          │
└─────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              OBSERVABILITY & MONITORING STACK                            │
│  • Prometheus: Metrics collection                                        │
│  • Grafana: Visualization dashboards                                     │
│  • ELK Stack: Centralized logging                                        │
│  • Jaeger: Distributed tracing                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 SERVICE CATEGORIES

### Priority 0 (P0): Infrastructure Foundation

**Critical infrastructure services that all other services depend on**

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| 01-common-library | N/A | N/A | Shared utilities, models, exceptions |
| 02-service-discovery | 8761 | PostgreSQL | Service registry via Consul |
| 03-api-gateway | 8000 | Redis | Single entry point, routing |
| 04-config-service | 8762 | PostgreSQL | Centralized configuration |

### Priority 1 (P1): Core Business Services

**Essential services for authentication, users, and notifications**

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| 05-auth-service | 8001 | PostgreSQL + Redis | OAuth2, JWT, RBAC |
| 06-user-service | 8002 | PostgreSQL | User profiles, preferences |
| 07-notification-service | 8003 | PostgreSQL + Redis | Email, SMS, Push |
| 08-file-storage-service | 8004 | PostgreSQL + S3 | File upload/download |
| 09-audit-service | 8013 | PostgreSQL + Elasticsearch | Audit logging |
| 10-email-service | 8015 | PostgreSQL | SMTP integration |
| 11-sms-service | 8016 | PostgreSQL | SMS gateway |
| 12-push-notification-service | 8017 | PostgreSQL + Redis | FCM, APNS |
| 13-websocket-service | 8018 | Redis | Real-time bidirectional |
| 14-event-bus-service | 8019 | Kafka | Event distribution |

### Priority 2 (P2): Business Domain Services

**E-commerce, payments, and business logic**

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| 15-payment-service | 8005 | PostgreSQL | Payment processing |
| 16-order-service | 8006 | PostgreSQL | Order management |
| 17-product-service | 8007 | PostgreSQL | Product catalog |
| 18-inventory-service | 8008 | PostgreSQL | Stock management |
| 19-cart-service | 8009 | Redis + PostgreSQL | Shopping cart |
| 20-shipping-service | 8010 | PostgreSQL | Shipping & logistics |
| 21-invoice-service | 8011 | PostgreSQL | Invoice generation |
| 22-discount-service | 8012 | PostgreSQL + Redis | Coupons, promotions |
| 23-review-service | 8014 | PostgreSQL | Product reviews |
| 24-wishlist-service | 8020 | PostgreSQL | User wishlists |
| 25-recommendation-service | 8021 | PostgreSQL + ML | ML recommendations |
| 26-search-service | 8022 | Elasticsearch | Full-text search |
| 27-analytics-service | 8023 | PostgreSQL + TimescaleDB | Business analytics |

### Priority 3 (P3): Advanced Features

**Advanced functionality and integrations**

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| 28-reporting-service | 8024 | PostgreSQL | PDF/Excel reports |
| 29-export-import-service | 8025 | PostgreSQL | Data migration |
| 30-backup-service | 8026 | PostgreSQL | Automated backups |
| 31-media-processing-service | 8027 | PostgreSQL + S3 | Video/image processing |
| 32-translation-service | 8028 | PostgreSQL | i18n support |
| 33-geolocation-service | 8029 | PostgreSQL + PostGIS | Maps, routing |
| 34-scheduling-service | 8030 | PostgreSQL | Cron jobs |
| 35-webhook-service | 8031 | PostgreSQL | Webhook management |
| 36-rate-limiting-service | 8032 | Redis | API protection |
| 37-cache-service | 8033 | Redis | Distributed caching |

### Priority 4 (P4): Specialized Services

**Niche and specialized functionality**

| Service | Port | Database | Purpose |
|---------|------|----------|---------|
| 38-ai-service | 8034 | PostgreSQL | AI/ML integration |
| 39-blockchain-service | 8035 | PostgreSQL | Blockchain integration |
| 40-iot-service | 8036 | PostgreSQL + TimescaleDB | IoT device management |
| 41-video-streaming-service | 8037 | PostgreSQL + S3 | Video streaming |
| 42-chat-service | 8038 | PostgreSQL + Redis | Real-time chat |
| 43-forum-service | 8039 | PostgreSQL | Discussion forums |
| 44-survey-service | 8040 | PostgreSQL | Survey creation |
| 45-cms-service | 8041 | PostgreSQL | Content management |
| 46-blog-service | 8042 | PostgreSQL | Blog platform |
| 47-ticket-service | 8043 | PostgreSQL | Support tickets |
| 48-appointment-service | 8044 | PostgreSQL | Booking system |
| 49-subscription-service | 8045 | PostgreSQL | Recurring billing |
| 50-loyalty-service | 8046 | PostgreSQL | Loyalty programs |
| 51-referral-service | 8047 | PostgreSQL | Referral tracking |
| 52-social-media-service | 8048 | PostgreSQL + MongoDB | Social features |

---

## 🏛️ COMMON ARCHITECTURE PATTERNS

### Standard Service Architecture

Every service follows this layered architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                          │
│  • FastAPI Routers (app/api/v1/*.py)                            │
│  • Request/Response Models (Pydantic schemas)                    │
│  • Input Validation                                              │
│  • Error Handling & HTTP Status Codes                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                        │
│  • Service Classes (app/services/*.py)                           │
│  • Business Rules & Workflows                                    │
│  • Transaction Management                                        │
│  • Integration with External Services                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                           │
│  • Repository Pattern                                            │
│  • SQLAlchemy Models (app/models/*.py)                           │
│  • Database Queries                                              │
│  • Caching Logic                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                        │
│  • Database Connection Pool                                      │
│  • Redis Client                                                  │
│  • Message Broker Connections                                    │
│  • External API Clients                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Standard Folder Structure

```
##-service-name/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Continuous Integration
│       ├── cd.yml                    # Continuous Deployment
│       └── security.yml              # Security scanning
│
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI application
│   ├── config.py                     # Configuration from env
│   ├── dependencies.py               # FastAPI dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints.py          # API endpoints
│   │       └── router.py             # Router aggregation
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py               # Database connection
│   │   ├── redis_client.py           # Redis connection
│   │   ├── security.py               # Auth helpers
│   │   ├── exceptions.py             # Custom exceptions
│   │   └── logging_config.py         # Structured logging
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── *.py                      # SQLAlchemy models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── *.py                      # Pydantic schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── *.py                      # Business logic
│   │
│   └── utils/
│       ├── __init__.py
│       └── *.py                      # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Test fixtures
│   ├── test_*.py                     # Unit tests
│   ├── integration/
│   │   └── test_*.py                 # Integration tests
│   └── e2e/
│       └── test_*.py                 # End-to-end tests
│
├── alembic/
│   ├── versions/                     # Database migrations
│   ├── env.py
│   └── script.py.mako
│
├── k8s/
│   ├── deployment.yaml               # Kubernetes deployment
│   ├── service.yaml                  # Kubernetes service
│   ├── configmap.yaml                # Configuration
│   ├── secrets.yaml                  # Secrets (template)
│   ├── ingress.yaml                  # Ingress rules
│   └── hpa.yaml                      # Horizontal Pod Autoscaler
│
├── scripts/
│   ├── __init__.py
│   ├── dev.py                        # Development server
│   ├── migrate.py                    # Database migrations
│   └── seed.py                       # Database seeding
│
├── .env.example                      # Environment template
├── .gitignore
├── alembic.ini                       # Alembic configuration
├── docker-compose.yml                # Local development
├── Dockerfile                        # Container image
├── pyproject.toml                    # Dependencies (Poetry)
├── pytest.ini                        # Pytest configuration
├── README.md                         # Service documentation
├── DEPLOYMENT.md                     # Deployment guide
└── LICENSE                           # MIT License
```

### Standard Dependencies (pyproject.toml)

```toml
[tool.poetry]
name = "service-name"
version = "1.0.0"
description = "Service description"
authors = ["Gravity Team <team@gravity.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
sqlalchemy = "^2.0.23"
alembic = "^1.13.0"
asyncpg = "^0.29.0"
redis = "^5.0.1"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
httpx = "^0.25.2"
structlog = "^23.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
black = "^23.11.0"
isort = "^5.12.0"
mypy = "^1.7.1"
ruff = "^0.1.6"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## 🔄 COMMUNICATION PATTERNS

### 1. Synchronous Communication (REST API)

**Use Cases:**
- Real-time user interactions
- Data retrieval
- CRUD operations
- Request-response patterns

**Example:**
```python
# API Gateway → Auth Service
async with httpx.AsyncClient() as client:
    response = await client.post(
        f"{settings.auth_service_url}/api/v1/auth/validate-token",
        json={"token": access_token},
        timeout=5.0
    )
    if response.status_code == 200:
        user_data = response.json()
```

**Best Practices:**
- Set timeouts (default: 5 seconds)
- Implement circuit breakers
- Use connection pooling
- Handle retries with exponential backoff
- Include correlation IDs for tracing

### 2. Asynchronous Communication (Event-Driven)

**Use Cases:**
- Background processing
- Notifications
- Data synchronization
- Eventual consistency

**Event Types:**

```python
# User Events
USER_CREATED = "user.created"
USER_UPDATED = "user.updated"
USER_DELETED = "user.deleted"

# Order Events
ORDER_CREATED = "order.created"
ORDER_CONFIRMED = "order.confirmed"
ORDER_SHIPPED = "order.shipped"
ORDER_DELIVERED = "order.delivered"
ORDER_CANCELLED = "order.cancelled"

# Payment Events
PAYMENT_INITIATED = "payment.initiated"
PAYMENT_COMPLETED = "payment.completed"
PAYMENT_FAILED = "payment.failed"

# Notification Events
NOTIFICATION_SENT = "notification.sent"
NOTIFICATION_DELIVERED = "notification.delivered"
NOTIFICATION_FAILED = "notification.failed"
```

**Example with RabbitMQ:**
```python
# Publisher (Order Service)
async def publish_order_created(order: Order):
    await message_broker.publish(
        exchange="gravity.events",
        routing_key="order.created",
        body={
            "order_id": order.id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "items": order.items,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Consumer (Notification Service)
@message_broker.subscribe("order.created")
async def handle_order_created(event: dict):
    await notification_service.send_order_confirmation(
        user_id=event["user_id"],
        order_id=event["order_id"]
    )
```

**Example with Kafka:**
```python
# Producer
async def publish_event(topic: str, key: str, value: dict):
    await kafka_producer.send(
        topic=topic,
        key=key.encode(),
        value=json.dumps(value).encode()
    )

# Consumer
async for message in kafka_consumer:
    event = json.loads(message.value.decode())
    await process_event(event)
```

### 3. WebSocket Communication

**Use Cases:**
- Real-time chat
- Live notifications
- Stock tickers
- Collaborative editing

**Example:**
```python
# WebSocket Service
from fastapi import WebSocket

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    await connection_manager.connect(user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(user_id, data)
    except WebSocketDisconnect:
        await connection_manager.disconnect(user_id)
```

### 4. GraphQL (Optional)

**Use Cases:**
- Complex data queries
- Mobile applications
- Flexible data fetching
- API aggregation

---

## 💾 DATA MANAGEMENT STRATEGY

### Database per Service Pattern

```
┌──────────────────────────────────────────────────────────────┐
│  SERVICE 1                                                   │
│  ├── Application Logic                                       │
│  └── Database 1 (PostgreSQL)                                 │
│      ├── Schema: service1                                    │
│      └── Tables: service1 specific                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SERVICE 2                                                   │
│  ├── Application Logic                                       │
│  └── Database 2 (PostgreSQL)                                 │
│      ├── Schema: service2                                    │
│      └── Tables: service2 specific                           │
└──────────────────────────────────────────────────────────────┘
```

### Data Sharing Strategies

#### 1. API Calls (Preferred)
```python
# User Service needs order data
async def get_user_with_orders(user_id: int) -> UserWithOrders:
    # Get user from local database
    user = await user_repo.get_by_id(user_id)
    
    # Get orders from Order Service via API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.order_service_url}/api/v1/orders",
            params={"user_id": user_id}
        )
        orders = response.json()
    
    return UserWithOrders(user=user, orders=orders)
```

#### 2. Event-Driven Data Replication
```python
# Order Service publishes event
await event_bus.publish("order.created", {
    "order_id": order.id,
    "user_id": order.user_id,
    "amount": order.total_amount
})

# Analytics Service consumes and stores
@event_bus.subscribe("order.created")
async def replicate_order_data(event: dict):
    await analytics_db.insert({
        "order_id": event["order_id"],
        "user_id": event["user_id"],
        "amount": event["amount"],
        "replicated_at": datetime.utcnow()
    })
```

#### 3. CQRS Pattern
```python
# Command Side (Write)
async def create_order(order_data: OrderCreate) -> Order:
    order = await order_repo.create(order_data)
    await event_bus.publish("order.created", order.dict())
    return order

# Query Side (Read)
async def get_order_details(order_id: int) -> OrderDetails:
    # Read from denormalized view
    return await read_model.get_order_details(order_id)
```

### Caching Strategy

```python
# Multi-level caching

# L1: Application-level cache (memory)
from cachetools import TTLCache
app_cache = TTLCache(maxsize=1000, ttl=300)

# L2: Redis cache (distributed)
@cache_result(ttl=600)
async def get_user(user_id: int) -> User:
    user = await redis.get(f"user:{user_id}")
    if user:
        return User.parse_raw(user)
    
    user = await user_repo.get_by_id(user_id)
    await redis.setex(
        f"user:{user_id}",
        600,
        user.json()
    )
    return user

# Cache invalidation
async def update_user(user_id: int, data: UserUpdate):
    user = await user_repo.update(user_id, data)
    await redis.delete(f"user:{user_id}")  # Invalidate cache
    return user
```

---

## 🔐 SECURITY ARCHITECTURE

### Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Client → API Gateway                                        │
│     POST /api/v1/auth/login                                     │
│     Body: {username, password}                                  │
│                                                                 │
│  2. API Gateway → Auth Service                                  │
│     Validate credentials                                        │
│                                                                 │
│  3. Auth Service → Database                                     │
│     Query user, verify password hash                            │
│                                                                 │
│  4. Auth Service → Client                                       │
│     Return: {                                                   │
│       access_token: "JWT...",                                   │
│       refresh_token: "...",                                     │
│       expires_in: 3600                                          │
│     }                                                            │
│                                                                 │
│  5. Client → API Gateway (Subsequent Requests)                  │
│     Header: Authorization: Bearer JWT...                        │
│                                                                 │
│  6. API Gateway validates JWT:                                  │
│     • Verify signature                                          │
│     • Check expiration                                          │
│     • Extract user info                                         │
│     • Forward to target service with user context               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Authorization (RBAC)

```python
# Role-Based Access Control

# Roles
ROLES = {
    "super_admin": ["*"],  # All permissions
    "admin": [
        "users:read", "users:write", "users:delete",
        "orders:read", "orders:write",
        "products:read", "products:write"
    ],
    "manager": [
        "users:read",
        "orders:read", "orders:write",
        "products:read"
    ],
    "customer": [
        "profile:read", "profile:write",
        "orders:read"
    ]
}

# Permission decorator
from functools import wraps

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not current_user.has_permission(permission):
                raise HTTPException(
                    status_code=403,
                    detail="Insufficient permissions"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@router.delete("/users/{user_id}")
@require_permission("users:delete")
async def delete_user(user_id: int):
    await user_service.delete(user_id)
```

### API Security

```python
# Rate Limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")
async def login(credentials: LoginRequest):
    pass

# CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Input Validation
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=50)
```

---

## 🚀 DEPLOYMENT ARCHITECTURE

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "${PORT}:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes (Production)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-name
  namespace: gravity
spec:
  replicas: 3
  selector:
    matchLabels:
      app: service-name
  template:
    metadata:
      labels:
        app: service-name
    spec:
      containers:
      - name: service-name
        image: gravity/service-name:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: service-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: service-name
  namespace: gravity
spec:
  selector:
    app: service-name
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: service-name-hpa
  namespace: gravity
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: service-name
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 📊 MONITORING & OBSERVABILITY

### Health Check Endpoint

```python
# All services MUST implement
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "service-name",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/detailed")
async def detailed_health_check():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "external_apis": await check_external_services()
    }
    
    all_healthy = all(checks.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Log with context
logger.info(
    "user_login_success",
    user_id=user.id,
    username=user.username,
    ip_address=request.client.host,
    user_agent=request.headers.get("user-agent")
)

# Log errors with stack trace
try:
    result = await risky_operation()
except Exception as e:
    logger.error(
        "operation_failed",
        operation="risky_operation",
        error=str(e),
        exc_info=True
    )
    raise
```

### Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge

# Request counter
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Response time histogram
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Active connections gauge
active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    path = request.url.path
    
    with request_duration.labels(method=method, endpoint=path).time():
        response = await call_next(request)
    
    request_count.labels(
        method=method,
        endpoint=path,
        status=response.status_code
    ).inc()
    
    return response
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

tracer = trace.get_tracer(__name__)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Manual spans
async def process_order(order_id: int):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        # Validate order
        with tracer.start_as_current_span("validate_order"):
            await validate_order(order_id)
        
        # Process payment
        with tracer.start_as_current_span("process_payment"):
            await payment_service.charge(order_id)
        
        span.set_attribute("order.status", "completed")
```

---

## 🎯 SERVICE-SPECIFIC ARCHITECTURES

### 05-Auth-Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTH SERVICE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API Layer                                                      │
│  ├── POST /api/v1/auth/register                                │
│  ├── POST /api/v1/auth/login                                   │
│  ├── POST /api/v1/auth/refresh                                 │
│  ├── POST /api/v1/auth/logout                                  │
│  ├── POST /api/v1/auth/validate-token                          │
│  ├── POST /api/v1/auth/password-reset                          │
│  └── GET  /api/v1/auth/me                                      │
│                                                                 │
│  Business Logic                                                 │
│  ├── Password hashing (bcrypt)                                 │
│  ├── JWT token generation/validation                           │
│  ├── OAuth2 providers (Google, GitHub)                         │
│  ├── Multi-factor authentication (TOTP)                        │
│  ├── Role-based access control (RBAC)                          │
│  └── Session management                                        │
│                                                                 │
│  Data Layer                                                     │
│  ├── PostgreSQL                                                │
│  │   ├── users table                                           │
│  │   ├── roles table                                           │
│  │   ├── permissions table                                     │
│  │   └── oauth_accounts table                                  │
│  └── Redis                                                      │
│      ├── Active sessions                                        │
│      ├── Refresh tokens                                         │
│      └── Rate limiting data                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 15-Payment-Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   PAYMENT SERVICE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API Layer                                                      │
│  ├── POST /api/v1/payments                                     │
│  ├── GET  /api/v1/payments/{id}                                │
│  ├── POST /api/v1/payments/{id}/refund                         │
│  └── GET  /api/v1/payments/history                             │
│                                                                 │
│  Business Logic                                                 │
│  ├── Payment processing (Stripe, PayPal)                       │
│  ├── Refund handling                                            │
│  ├── Payment verification                                       │
│  ├── Idempotency checking                                       │
│  └── Fraud detection                                            │
│                                                                 │
│  Integration Layer                                              │
│  ├── Stripe API client                                         │
│  ├── PayPal API client                                         │
│  ├── Bank API integrations                                      │
│  └── Cryptocurrency gateways                                    │
│                                                                 │
│  Data Layer                                                     │
│  ├── PostgreSQL                                                │
│  │   ├── payments table                                        │
│  │   ├── transactions table                                    │
│  │   ├── refunds table                                         │
│  │   └── payment_methods table                                 │
│  └── Redis                                                      │
│      └── Idempotency keys cache                                │
│                                                                 │
│  Event Publishing                                               │
│  ├── payment.initiated                                          │
│  ├── payment.completed                                          │
│  ├── payment.failed                                             │
│  └── payment.refunded                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 16-Order-Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORDER SERVICE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API Layer                                                      │
│  ├── POST /api/v1/orders                                       │
│  ├── GET  /api/v1/orders/{id}                                  │
│  ├── PUT  /api/v1/orders/{id}/status                           │
│  ├── POST /api/v1/orders/{id}/cancel                           │
│  └── GET  /api/v1/orders/user/{user_id}                        │
│                                                                 │
│  Business Logic (Saga Pattern)                                  │
│  ├── Step 1: Create order (PENDING)                            │
│  ├── Step 2: Reserve inventory                                 │
│  │   └── Call: Inventory Service                               │
│  ├── Step 3: Process payment                                   │
│  │   └── Call: Payment Service                                 │
│  ├── Step 4: Confirm order (CONFIRMED)                         │
│  └── Compensation: Rollback on failure                         │
│                                                                 │
│  State Machine                                                  │
│  PENDING → CONFIRMED → PROCESSING → SHIPPED → DELIVERED        │
│     ↓                                                           │
│  CANCELLED ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←                │
│                                                                 │
│  Data Layer                                                     │
│  ├── PostgreSQL                                                │
│  │   ├── orders table                                          │
│  │   ├── order_items table                                     │
│  │   ├── order_status_history table                            │
│  │   └── saga_state table                                      │
│  └── Redis                                                      │
│      └── Order locks (distributed locking)                     │
│                                                                 │
│  Event Publishing                                               │
│  ├── order.created                                              │
│  ├── order.confirmed                                            │
│  ├── order.shipped                                              │
│  ├── order.delivered                                            │
│  └── order.cancelled                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 26-Search-Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   SEARCH SERVICE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API Layer                                                      │
│  ├── GET  /api/v1/search?q=query                               │
│  ├── POST /api/v1/search/advanced                              │
│  ├── GET  /api/v1/search/suggestions                           │
│  └── GET  /api/v1/search/autocomplete                          │
│                                                                 │
│  Business Logic                                                 │
│  ├── Full-text search                                           │
│  ├── Fuzzy matching                                             │
│  ├── Faceted search                                             │
│  ├── Relevance scoring                                          │
│  ├── Query parsing                                              │
│  └── Result ranking                                             │
│                                                                 │
│  Data Layer                                                     │
│  ├── Elasticsearch                                             │
│  │   ├── products index                                        │
│  │   ├── users index                                           │
│  │   └── content index                                         │
│  └── Redis                                                      │
│      ├── Search result cache                                    │
│      └── Popular searches                                       │
│                                                                 │
│  Event Consumers (Data Sync)                                    │
│  ├── product.created → Index product                           │
│  ├── product.updated → Update index                            │
│  └── product.deleted → Remove from index                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 SCALABILITY PATTERNS

### Horizontal Scaling

```yaml
# Kubernetes HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: service-name
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

### Database Sharding

```python
# Shard by user_id
def get_shard_key(user_id: int) -> int:
    return user_id % settings.num_shards

async def get_user_connection(user_id: int):
    shard = get_shard_key(user_id)
    return database_pool[shard]

# Usage
async def get_user(user_id: int) -> User:
    db = await get_user_connection(user_id)
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

### Read Replicas

```python
# Master-slave database configuration
class DatabaseRouter:
    def __init__(self):
        self.master = create_engine(settings.master_db_url)
        self.replicas = [
            create_engine(url) for url in settings.replica_db_urls
        ]
    
    async def get_write_connection(self):
        return self.master
    
    async def get_read_connection(self):
        # Round-robin load balancing
        replica = random.choice(self.replicas)
        return replica

# Usage
async def create_user(user_data: UserCreate) -> User:
    db = await db_router.get_write_connection()
    # Write to master
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    return user

async def get_user(user_id: int) -> User:
    db = await db_router.get_read_connection()
    # Read from replica
    return await db.get(User, user_id)
```

---

## 🔄 CI/CD PIPELINE

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run linters
        run: |
          poetry run black --check app/
          poetry run isort --check app/
          poetry run mypy app/
      
      - name: Run tests
        run: |
          poetry run pytest tests/ -v --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        run: |
          pip install bandit safety
          bandit -r app/
          safety check

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t gravity/service-name:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          docker push gravity/service-name:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/service-name \
            service-name=gravity/service-name:${{ github.sha }}
```

---

## 📚 BEST PRACTICES SUMMARY

### ✅ DO (Always)

1. **Independence**
   - Own database per service
   - Environment-based configuration
   - No direct service imports

2. **Security**
   - Use parametrized queries
   - Implement rate limiting
   - Validate all inputs
   - Never hardcode secrets

3. **Testing**
   - Minimum 95% coverage
   - Write tests first (TDD)
   - Integration tests for APIs
   - Load testing for critical paths

4. **Documentation**
   - README with quick start
   - API documentation (Swagger)
   - Deployment guide
   - Architecture diagrams

5. **Monitoring**
   - Health check endpoints
   - Structured logging
   - Metrics collection
   - Distributed tracing

### ❌ DON'T (Never)

1. **Anti-patterns**
   - Shared databases
   - Direct service imports
   - Hardcoded configurations
   - Synchronous calls for long operations

2. **Security**
   - String interpolation in SQL
   - Plaintext passwords
   - Exposed secrets
   - Missing input validation

3. **Code Quality**
   - Missing type hints
   - No error handling
   - Bare except clauses
   - Non-English code/comments

---

## 🎓 CONCLUSION

This architecture framework provides:

✅ **52 independent microservices** ready for any project  
✅ **Proven patterns** for scalability and reliability  
✅ **Security best practices** built-in from day one  
✅ **Complete documentation** for each service  
✅ **Production-ready** deployment configurations  
✅ **Monitoring and observability** out of the box  

**Next Steps:**
1. Choose services based on project needs
2. Follow service-specific architecture
3. Implement using standard patterns
4. Deploy independently
5. Monitor and scale as needed

---

**Questions? See:**
- `TEAM_PROMPT.md` - Team standards and practices
- `SERVICES_INDEX.md` - Complete service catalog
- `TEAM_START_GUIDE.md` - Development guide (Persian)
- Individual service `README.md` files

---

*Last Updated: November 10, 2025*  
*Maintained by: Gravity Elite Engineering Team*
