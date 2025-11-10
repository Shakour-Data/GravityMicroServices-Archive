<!--
================================================================================
FILE IDENTITY
================================================================================
Project      : Gravity Common Library
File         : README.md
Description  : Shared Python utilities and models for all Gravity microservices
Language     : English (UK)
Document Type: Package Documentation

================================================================================
AUTHORSHIP & CONTRIBUTION
================================================================================
Primary Author    : Dr. Sarah Chen (Chief Architect)
Contributors      : All 9 team members
Team Standard     : Elite Engineers (IQ 180+, 15+ years experience)

================================================================================
TIMELINE & EFFORT
================================================================================
Created Date      : 2025-11-07 17:30 UTC
Last Modified     : 2025-11-07 17:30 UTC
Writing Time      : 2 hours 0 minutes
Total Cost        : 2 × $150 = $300.00 USD

================================================================================
VERSION HISTORY
================================================================================
v1.0.0 - 2025-11-07 - Dr. Sarah Chen - Initial common library documentation

================================================================================
LICENSE & COPYRIGHT
================================================================================
Copyright (c) 2025 Gravity MicroServices Platform
License: MIT License
Repository: https://github.com/Shakour-Data/gravity-common
================================================================================
-->

# 📚 Gravity Common Library

**Shared Python utilities, models, and helpers for all Gravity microservices**

---

## Overview

`gravity-common` is a shared Python package containing reusable code for all Gravity microservices. It ensures consistency, reduces duplication, and provides battle-tested utilities for common tasks.

### Key Features

✅ **Database Utilities** - SQLAlchemy async engine, session management  
✅ **Redis Client** - Async Redis connection with helpers  
✅ **Security Utilities** - Password hashing, JWT helpers, token validation  
✅ **Common Models** - Base models, mixins (timestamps, soft delete)  
✅ **Exceptions** - Standard exception hierarchy  
✅ **Logging Config** - Structured JSON logging  
✅ **Utility Functions** - Date/time, validation, helpers  

---

## Installation

### From Git Repository (Recommended)

```bash
# Install latest version
poetry add git+https://github.com/Shakour-Data/gravity-common.git

# Install specific version
poetry add git+https://github.com/Shakour-Data/gravity-common.git@v1.0.0
```

### From Local Path (Development)

```bash
# For local development
poetry add ../common-library
```

---

## Quick Start

### Database Connection

```python
from gravity_common.database import get_engine, get_session_factory

# Create async engine
engine = get_engine("postgresql+asyncpg://user:pass@localhost/mydb")

# Create session factory
SessionLocal = get_session_factory(engine)

# Use in FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
```

### Redis Client

```python
from gravity_common.redis_client import get_redis_client

# Get Redis client
redis = await get_redis_client("redis://localhost:6379/0")

# Use Redis
await redis.set("key", "value", ex=300)  # Expires in 5 minutes
value = await redis.get("key")
```

### Security Utilities

```python
from gravity_common.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)

# Hash password
hashed = get_password_hash("my_password")

# Verify password
is_valid = verify_password("my_password", hashed)

# Create JWT token
token = create_access_token(
    data={"sub": "user@example.com", "user_id": 1},
    secret_key="your-secret-key",
    expires_delta=timedelta(minutes=30)
)

# Verify JWT token
payload = verify_token(token, "your-secret-key")
```

### Base Models

```python
from gravity_common.models import BaseModel, TimestampMixin, SoftDeleteMixin
from sqlalchemy import Column, Integer, String

# Model with timestamps
class User(BaseModel, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

# Model with soft delete
class Post(BaseModel, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
```

### Exceptions

```python
from gravity_common.exceptions import (
    NotFoundException,
    ValidationException,
    UnauthorizedException,
    DatabaseException
)

# Raise exceptions
if not user:
    raise NotFoundException("User not found")

if not email_valid:
    raise ValidationException("Invalid email format")

if not authenticated:
    raise UnauthorizedException("Authentication required")
```

### Logging

```python
from gravity_common.logging_config import setup_logging
import logging

# Setup structured logging
setup_logging(
    service_name="my-service",
    log_level="INFO",
    json_format=True
)

logger = logging.getLogger(__name__)

# Log messages
logger.info("User logged in", extra={"user_id": 1, "email": "user@example.com"})
logger.error("Database error", extra={"error": str(e)}, exc_info=True)
```

### Utility Functions

```python
from gravity_common.utils import (
    generate_uuid,
    parse_datetime,
    format_datetime,
    validate_email,
    slugify
)

# Generate UUID
id = generate_uuid()  # Returns: str

# Parse datetime
dt = parse_datetime("2025-11-07T17:30:00Z")

# Format datetime
formatted = format_datetime(dt)  # Returns: "2025-11-07T17:30:00Z"

# Validate email
is_valid = validate_email("user@example.com")  # Returns: True

# Slugify text
slug = slugify("Hello World!")  # Returns: "hello-world"
```

---

## API Reference

### `gravity_common.database`

#### `get_engine(database_url: str, **kwargs) -> AsyncEngine`

Create SQLAlchemy async engine.

**Parameters:**
- `database_url` (str): Database connection URL
- `**kwargs`: Additional engine options

**Returns:** `AsyncEngine`

**Example:**
```python
engine = get_engine(
    "postgresql+asyncpg://user:pass@localhost/mydb",
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)
```

---

#### `get_session_factory(engine: AsyncEngine) -> sessionmaker`

Create async session factory.

**Parameters:**
- `engine` (AsyncEngine): Database engine

**Returns:** `sessionmaker`

**Example:**
```python
SessionLocal = get_session_factory(engine)

async with SessionLocal() as session:
    result = await session.execute(select(User))
    users = result.scalars().all()
```

---

### `gravity_common.redis_client`

#### `get_redis_client(redis_url: str, **kwargs) -> Redis`

Create Redis async client.

**Parameters:**
- `redis_url` (str): Redis connection URL
- `**kwargs`: Additional Redis options

**Returns:** `Redis`

**Example:**
```python
redis = await get_redis_client(
    "redis://:password@localhost:6379/0",
    decode_responses=True,
    socket_keepalive=True
)

# Set value with expiration
await redis.setex("session:123", 3600, "user_data")

# Get value
value = await redis.get("session:123")

# Delete key
await redis.delete("session:123")

# Check existence
exists = await redis.exists("session:123")
```

---

### `gravity_common.security`

#### `get_password_hash(password: str) -> str`

Hash password using bcrypt.

**Parameters:**
- `password` (str): Plain text password

**Returns:** Hashed password (str)

**Example:**
```python
hashed = get_password_hash("MySecurePassword123!")
# Returns: "$2b$12$..."
```

---

#### `verify_password(plain_password: str, hashed_password: str) -> bool`

Verify password against hash.

**Parameters:**
- `plain_password` (str): Plain text password
- `hashed_password` (str): Bcrypt hash

**Returns:** True if valid, False otherwise

**Example:**
```python
is_valid = verify_password("MySecurePassword123!", hashed)
```

---

#### `create_access_token(data: dict, secret_key: str, expires_delta: Optional[timedelta] = None) -> str`

Create JWT access token.

**Parameters:**
- `data` (dict): Payload data
- `secret_key` (str): JWT secret key
- `expires_delta` (timedelta, optional): Token expiration

**Returns:** JWT token (str)

**Example:**
```python
from datetime import timedelta

token = create_access_token(
    data={"sub": "user@example.com", "role": "admin"},
    secret_key="your-secret-key",
    expires_delta=timedelta(minutes=30)
)
```

---

#### `verify_token(token: str, secret_key: str) -> dict`

Verify and decode JWT token.

**Parameters:**
- `token` (str): JWT token
- `secret_key` (str): JWT secret key

**Returns:** Decoded payload (dict)

**Raises:** `InvalidTokenException` if invalid

**Example:**
```python
try:
    payload = verify_token(token, "your-secret-key")
    user_email = payload["sub"]
except InvalidTokenException:
    # Handle invalid token
    pass
```

---

### `gravity_common.models`

#### `BaseModel`

SQLAlchemy declarative base for all models.

```python
from gravity_common.models import BaseModel
from sqlalchemy import Column, Integer, String

class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

---

#### `TimestampMixin`

Adds `created_at` and `updated_at` columns.

```python
class User(BaseModel, TimestampMixin):
    # Automatically has:
    # - created_at: DateTime (auto-set on insert)
    # - updated_at: DateTime (auto-updated)
    pass
```

---

#### `SoftDeleteMixin`

Adds `deleted_at` column for soft deletes.

```python
class Post(BaseModel, SoftDeleteMixin):
    # Automatically has:
    # - deleted_at: DateTime (nullable)
    # - is_deleted property
    pass

# Soft delete
post.deleted_at = datetime.utcnow()
await session.commit()

# Check if deleted
if post.is_deleted:
    print("Post is deleted")
```

---

### `gravity_common.exceptions`

#### Exception Hierarchy

```
GravityException (Base)
├── NotFoundException (404)
├── ValidationException (400)
├── UnauthorizedException (401)
├── ForbiddenException (403)
├── ConflictException (409)
├── DatabaseException (500)
└── ExternalServiceException (503)
```

**Usage:**
```python
from gravity_common.exceptions import NotFoundException

user = await get_user(user_id)
if not user:
    raise NotFoundException(f"User {user_id} not found")
```

---

### `gravity_common.logging_config`

#### `setup_logging(service_name: str, log_level: str = "INFO", json_format: bool = True)`

Configure structured logging.

**Parameters:**
- `service_name` (str): Service name for logs
- `log_level` (str): Log level (DEBUG/INFO/WARNING/ERROR)
- `json_format` (bool): Use JSON format

**Example:**
```python
setup_logging(
    service_name="auth-service",
    log_level="INFO",
    json_format=True
)

logger = logging.getLogger(__name__)
logger.info("Service started", extra={"port": 8081})
```

**JSON Output:**
```json
{
  "timestamp": "2025-11-07T17:30:00Z",
  "level": "INFO",
  "service": "auth-service",
  "message": "Service started",
  "port": 8081
}
```

---

### `gravity_common.utils`

#### Common Utilities

```python
# UUID generation
id = generate_uuid()  # Returns: "a1b2c3d4-..."

# Email validation
is_valid = validate_email("user@example.com")  # True
is_valid = validate_email("invalid")  # False

# Slugify text
slug = slugify("Hello World! 123")  # "hello-world-123"

# Parse datetime
dt = parse_datetime("2025-11-07T17:30:00Z")

# Format datetime
formatted = format_datetime(datetime.utcnow())

# Generate random string
random_str = generate_random_string(length=16)
```

---

## Development

### Setup

```bash
cd common-library
poetry install
```

### Run Tests

```bash
pytest tests/ -v --cov=gravity_common
```

### Build Package

```bash
poetry build
```

### Publish (Internal)

```bash
# Tag version
git tag v1.0.0
git push origin v1.0.0

# Other services can now install:
# poetry add git+https://github.com/Shakour-Data/gravity-common.git@v1.0.0
```

---

## Best Practices

### 1. Import Specific Functions

```python
# ✅ GOOD - Specific imports
from gravity_common.security import get_password_hash, verify_password

# ❌ BAD - Star imports
from gravity_common.security import *
```

### 2. Use Type Hints

```python
from gravity_common.database import get_engine
from sqlalchemy.ext.asyncio import AsyncEngine

# ✅ GOOD - Type hints
engine: AsyncEngine = get_engine(database_url)
```

### 3. Handle Exceptions

```python
from gravity_common.exceptions import NotFoundException

# ✅ GOOD - Catch specific exceptions
try:
    user = await get_user(user_id)
except NotFoundException:
    return {"error": "User not found"}
```

---

## Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backwards compatible)
- **PATCH:** Bug fixes

**Current Version:** 1.0.0

---

## Contributing

1. Create feature branch: `git checkout -b feature/new-utility`
2. Write tests for new code
3. Ensure 95%+ coverage: `pytest --cov`
4. Update documentation
5. Submit pull request

---

## License

MIT License - See [LICENSE](LICENSE) file

---

## Support

- **Repository:** https://github.com/Shakour-Data/gravity-common
- **Issues:** https://github.com/Shakour-Data/gravity-common/issues
- **Documentation:** https://docs.gravity-platform.com/common-library

---

**Last Updated:** 2025-11-07  
**Version:** 1.0.0  
**Maintainer:** Dr. Sarah Chen (Chief Architect)
