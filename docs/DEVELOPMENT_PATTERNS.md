# 🎨 DEVELOPMENT PATTERNS & BEST PRACTICES

> **Proven patterns and practices for building Gravity microservices**

**Version:** 1.0.0  
**Last Updated:** November 10, 2025

---

## 📑 TABLE OF CONTENTS

1. [API Development Patterns](#api-development-patterns)
2. [Service Layer Patterns](#service-layer-patterns)
3. [Repository Pattern](#repository-pattern)
4. [Error Handling Patterns](#error-handling-patterns)
5. [Testing Patterns](#testing-patterns)
6. [Caching Patterns](#caching-patterns)
7. [Event-Driven Patterns](#event-driven-patterns)
8. [Authentication Patterns](#authentication-patterns)

---

## 🚀 API DEVELOPMENT PATTERNS

### RESTful Endpoint Pattern

```python
"""
Standard RESTful API endpoint pattern.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceResponse
from app.schemas.response import ApiResponse, PaginatedResponse
from app.services.resource_service import ResourceService
from app.models.user import User
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/resources", tags=["Resources"])


# =============================================================================
# CREATE - POST /resources
# =============================================================================
@router.post(
    "/",
    response_model=ApiResponse[ResourceResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new resource",
    description="Create a new resource with the provided data"
)
async def create_resource(
    resource_data: ResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApiResponse[ResourceResponse]:
    """
    Create a new resource.
    
    Args:
        resource_data: Resource creation data
        db: Database session
        current_user: Authenticated user
    
    Returns:
        ApiResponse containing created resource
    
    Raises:
        HTTPException: If creation fails
    """
    logger.info(
        "create_resource_request",
        user_id=current_user.id,
        resource_name=resource_data.name
    )
    
    try:
        service = ResourceService(db)
        resource = await service.create(resource_data, current_user.id)
        
        logger.info(
            "resource_created",
            resource_id=resource.id,
            user_id=current_user.id
        )
        
        return ApiResponse(
            success=True,
            message="Resource created successfully",
            data=ResourceResponse.from_orm(resource)
        )
    
    except ValueError as e:
        logger.warning("resource_creation_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("resource_creation_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create resource"
        )


# =============================================================================
# READ - GET /resources/{id}
# =============================================================================
@router.get(
    "/{resource_id}",
    response_model=ApiResponse[ResourceResponse],
    summary="Get resource by ID",
    description="Retrieve a single resource by its ID"
)
async def get_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApiResponse[ResourceResponse]:
    """
    Get resource by ID.
    
    Args:
        resource_id: Resource ID
        db: Database session
        current_user: Authenticated user
    
    Returns:
        ApiResponse containing resource
    
    Raises:
        HTTPException: If resource not found
    """
    service = ResourceService(db)
    resource = await service.get_by_id(resource_id)
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )
    
    return ApiResponse(
        success=True,
        data=ResourceResponse.from_orm(resource)
    )


# =============================================================================
# READ - GET /resources (List with Pagination)
# =============================================================================
@router.get(
    "/",
    response_model=PaginatedResponse[ResourceResponse],
    summary="List resources",
    description="Get paginated list of resources"
)
async def list_resources(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    search: str = Query(None, description="Search query"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PaginatedResponse[ResourceResponse]:
    """
    List resources with pagination and search.
    
    Args:
        skip: Number of items to skip
        limit: Number of items to return
        search: Optional search query
        db: Database session
        current_user: Authenticated user
    
    Returns:
        PaginatedResponse containing resources
    """
    service = ResourceService(db)
    resources, total = await service.list(
        skip=skip,
        limit=limit,
        search=search,
        user_id=current_user.id
    )
    
    return PaginatedResponse(
        success=True,
        data=[ResourceResponse.from_orm(r) for r in resources],
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


# =============================================================================
# UPDATE - PUT /resources/{id}
# =============================================================================
@router.put(
    "/{resource_id}",
    response_model=ApiResponse[ResourceResponse],
    summary="Update resource",
    description="Update an existing resource"
)
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApiResponse[ResourceResponse]:
    """
    Update resource.
    
    Args:
        resource_id: Resource ID
        resource_data: Resource update data
        db: Database session
        current_user: Authenticated user
    
    Returns:
        ApiResponse containing updated resource
    
    Raises:
        HTTPException: If resource not found or update fails
    """
    service = ResourceService(db)
    
    try:
        resource = await service.update(
            resource_id,
            resource_data,
            current_user.id
        )
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with ID {resource_id} not found"
            )
        
        logger.info(
            "resource_updated",
            resource_id=resource_id,
            user_id=current_user.id
        )
        
        return ApiResponse(
            success=True,
            message="Resource updated successfully",
            data=ResourceResponse.from_orm(resource)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# =============================================================================
# DELETE - DELETE /resources/{id}
# =============================================================================
@router.delete(
    "/{resource_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete resource",
    description="Delete an existing resource"
)
async def delete_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApiResponse[None]:
    """
    Delete resource.
    
    Args:
        resource_id: Resource ID
        db: Database session
        current_user: Authenticated user
    
    Returns:
        ApiResponse with success message
    
    Raises:
        HTTPException: If resource not found
    """
    service = ResourceService(db)
    
    deleted = await service.delete(resource_id, current_user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found"
        )
    
    logger.info(
        "resource_deleted",
        resource_id=resource_id,
        user_id=current_user.id
    )
    
    return ApiResponse(
        success=True,
        message="Resource deleted successfully"
    )
```

### Response Schemas

```python
"""
Standard response schemas.
"""
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    Generic API response wrapper.
    
    Provides consistent response structure across all endpoints.
    """
    success: bool = Field(..., description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Human-readable message")
    data: Optional[T] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"id": 1, "name": "Example"},
                "timestamp": "2025-11-10T10:00:00Z"
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response wrapper.
    
    Used for list endpoints with pagination.
    """
    success: bool = True
    data: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    
    def __init__(self, **data):
        if 'total_pages' not in data:
            data['total_pages'] = (data['total'] + data['page_size'] - 1) // data['page_size']
        super().__init__(**data)
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [{"id": 1}, {"id": 2}],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## 🔧 SERVICE LAYER PATTERNS

### Service Class Pattern

```python
"""
Standard service layer pattern.
"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
import structlog

from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.core.exceptions import ResourceNotFoundException, DuplicateResourceException

logger = structlog.get_logger()


class ResourceService:
    """
    Service layer for resource business logic.
    
    Handles all business logic for resource operations.
    Separates business logic from API layer.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def create(
        self,
        resource_data: ResourceCreate,
        user_id: int
    ) -> Resource:
        """
        Create a new resource.
        
        Args:
            resource_data: Resource creation data
            user_id: ID of user creating resource
        
        Returns:
            Created resource
        
        Raises:
            DuplicateResourceException: If resource already exists
        """
        # Check for duplicate
        existing = await self._get_by_name(resource_data.name)
        if existing:
            raise DuplicateResourceException(
                f"Resource with name '{resource_data.name}' already exists"
            )
        
        # Create resource
        resource = Resource(
            **resource_data.model_dump(),
            created_by=user_id
        )
        
        self.db.add(resource)
        await self.db.commit()
        await self.db.refresh(resource)
        
        logger.info(
            "resource_created",
            resource_id=resource.id,
            name=resource.name,
            created_by=user_id
        )
        
        return resource
    
    async def get_by_id(self, resource_id: int) -> Optional[Resource]:
        """
        Get resource by ID.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            Resource if found, None otherwise
        """
        result = await self.db.execute(
            select(Resource).where(Resource.id == resource_id)
        )
        return result.scalar_one_or_none()
    
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> Tuple[List[Resource], int]:
        """
        List resources with pagination and search.
        
        Args:
            skip: Number of items to skip
            limit: Number of items to return
            search: Optional search query
            user_id: Optional filter by user ID
        
        Returns:
            Tuple of (resources list, total count)
        """
        # Build query
        query = select(Resource)
        
        # Add filters
        if search:
            query = query.where(
                or_(
                    Resource.name.ilike(f"%{search}%"),
                    Resource.description.ilike(f"%{search}%")
                )
            )
        
        if user_id:
            query = query.where(Resource.created_by == user_id)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Add pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        resources = result.scalars().all()
        
        return list(resources), total or 0
    
    async def update(
        self,
        resource_id: int,
        resource_data: ResourceUpdate,
        user_id: int
    ) -> Optional[Resource]:
        """
        Update resource.
        
        Args:
            resource_id: Resource ID
            resource_data: Resource update data
            user_id: ID of user updating resource
        
        Returns:
            Updated resource if found, None otherwise
        
        Raises:
            DuplicateResourceException: If name conflicts with existing resource
        """
        resource = await self.get_by_id(resource_id)
        
        if not resource:
            return None
        
        # Check for name conflict
        if resource_data.name and resource_data.name != resource.name:
            existing = await self._get_by_name(resource_data.name)
            if existing and existing.id != resource_id:
                raise DuplicateResourceException(
                    f"Resource with name '{resource_data.name}' already exists"
                )
        
        # Update fields
        update_data = resource_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resource, field, value)
        
        resource.updated_by = user_id
        
        await self.db.commit()
        await self.db.refresh(resource)
        
        logger.info(
            "resource_updated",
            resource_id=resource_id,
            updated_by=user_id
        )
        
        return resource
    
    async def delete(self, resource_id: int, user_id: int) -> bool:
        """
        Delete resource.
        
        Args:
            resource_id: Resource ID
            user_id: ID of user deleting resource
        
        Returns:
            True if deleted, False if not found
        """
        resource = await self.get_by_id(resource_id)
        
        if not resource:
            return False
        
        await self.db.delete(resource)
        await self.db.commit()
        
        logger.info(
            "resource_deleted",
            resource_id=resource_id,
            deleted_by=user_id
        )
        
        return True
    
    async def _get_by_name(self, name: str) -> Optional[Resource]:
        """Get resource by name (private helper)."""
        result = await self.db.execute(
            select(Resource).where(Resource.name == name)
        )
        return result.scalar_one_or_none()
```

---

## 🗄️ REPOSITORY PATTERN

```python
"""
Repository pattern for data access.
"""
from typing import List, Optional, Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar('T', bound=DeclarativeMeta)


class BaseRepository(Generic[T]):
    """
    Generic repository for CRUD operations.
    
    Provides common database operations for any model.
    """
    
    def __init__(self, model: Type[T], db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[T]:
        """Get all entities with pagination."""
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def count(self) -> int:
        """Count total entities."""
        result = await self.db.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()
    
    async def create(self, entity: T) -> T:
        """Create new entity."""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def update(self, entity: T) -> T:
        """Update existing entity."""
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def delete(self, entity: T) -> None:
        """Delete entity."""
        await self.db.delete(entity)
        await self.db.commit()
    
    async def exists(self, id: int) -> bool:
        """Check if entity exists."""
        result = await self.db.execute(
            select(func.count()).where(self.model.id == id).select_from(self.model)
        )
        return result.scalar_one() > 0


# Usage example
class UserRepository(BaseRepository[User]):
    """User-specific repository."""
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_active_users(self) -> List[User]:
        """Get all active users."""
        result = await self.db.execute(
            select(User).where(User.is_active == True)
        )
        return list(result.scalars().all())
```

---

## ⚠️ ERROR HANDLING PATTERNS

### Custom Exceptions

```python
"""
Custom exception hierarchy.
"""


class GravityException(Exception):
    """Base exception for all Gravity services."""
    pass


class ResourceNotFoundException(GravityException):
    """Raised when a resource is not found."""
    pass


class DuplicateResourceException(GravityException):
    """Raised when trying to create a duplicate resource."""
    pass


class ValidationException(GravityException):
    """Raised when validation fails."""
    pass


class AuthenticationException(GravityException):
    """Raised when authentication fails."""
    pass


class AuthorizationException(GravityException):
    """Raised when user doesn't have permission."""
    pass
```

### Global Exception Handler

```python
"""
Global exception handlers for FastAPI.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog

from app.core.exceptions import (
    GravityException,
    ResourceNotFoundException,
    DuplicateResourceException,
    ValidationException,
    AuthenticationException,
    AuthorizationException
)

logger = structlog.get_logger()


def setup_exception_handlers(app):
    """Setup global exception handlers."""
    
    @app.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
        """Handle resource not found exceptions."""
        logger.warning("resource_not_found", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "error": "ResourceNotFound",
                "detail": str(exc)
            }
        )
    
    @app.exception_handler(DuplicateResourceException)
    async def duplicate_resource_handler(request: Request, exc: DuplicateResourceException):
        """Handle duplicate resource exceptions."""
        logger.warning("duplicate_resource", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": "DuplicateResource",
                "detail": str(exc)
            }
        )
    
    @app.exception_handler(ValidationException)
    async def validation_handler(request: Request, exc: ValidationException):
        """Handle validation exceptions."""
        logger.warning("validation_error", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": "ValidationError",
                "detail": str(exc)
            }
        )
    
    @app.exception_handler(AuthenticationException)
    async def authentication_handler(request: Request, exc: AuthenticationException):
        """Handle authentication exceptions."""
        logger.warning("authentication_failed", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "error": "AuthenticationFailed",
                "detail": str(exc)
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @app.exception_handler(AuthorizationException)
    async def authorization_handler(request: Request, exc: AuthorizationException):
        """Handle authorization exceptions."""
        logger.warning("authorization_failed", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "success": False,
                "error": "Forbidden",
                "detail": str(exc)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        logger.warning("request_validation_error", errors=exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": "ValidationError",
                "detail": exc.errors()
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error("unexpected_error", error=str(exc), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "InternalServerError",
                "detail": "An unexpected error occurred"
            }
        )
```

---

## 🧪 TESTING PATTERNS

### Test Fixtures

```python
"""
Standard test fixtures.
"""
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient

from app.main import app
from app.core.database import Base, get_db
from app.config import settings


@pytest_asyncio.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine(
        settings.test_database_url,
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_db):
    """Get database session for tests."""
    async_session = async_sessionmaker(
        test_db,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    """Get test client."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(test_user):
    """Get authentication headers."""
    from app.core.security import create_access_token
    
    token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
```

### Unit Tests

```python
"""
Unit tests for service layer.
"""
import pytest
from app.services.resource_service import ResourceService
from app.schemas.resource import ResourceCreate
from app.core.exceptions import DuplicateResourceException


@pytest.mark.asyncio
async def test_create_resource(db_session):
    """Test creating a resource."""
    service = ResourceService(db_session)
    
    data = ResourceCreate(
        name="Test Resource",
        description="Test description"
    )
    
    resource = await service.create(data, user_id=1)
    
    assert resource.id is not None
    assert resource.name == "Test Resource"
    assert resource.description == "Test description"
    assert resource.created_by == 1


@pytest.mark.asyncio
async def test_create_duplicate_resource(db_session):
    """Test creating duplicate resource raises exception."""
    service = ResourceService(db_session)
    
    data = ResourceCreate(name="Duplicate", description="Test")
    
    await service.create(data, user_id=1)
    
    with pytest.raises(DuplicateResourceException):
        await service.create(data, user_id=1)


@pytest.mark.asyncio
async def test_get_resource_by_id(db_session):
    """Test getting resource by ID."""
    service = ResourceService(db_session)
    
    data = ResourceCreate(name="Test", description="Test")
    created = await service.create(data, user_id=1)
    
    resource = await service.get_by_id(created.id)
    
    assert resource is not None
    assert resource.id == created.id
    assert resource.name == "Test"
```

### Integration Tests

```python
"""
Integration tests for API endpoints.
"""
import pytest


@pytest.mark.asyncio
async def test_create_resource_endpoint(client, auth_headers):
    """Test POST /api/v1/resources endpoint."""
    response = await client.post(
        "/api/v1/resources",
        json={
            "name": "Test Resource",
            "description": "Test description"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Test Resource"


@pytest.mark.asyncio
async def test_get_resource_endpoint(client, auth_headers):
    """Test GET /api/v1/resources/{id} endpoint."""
    # Create resource first
    create_response = await client.post(
        "/api/v1/resources",
        json={"name": "Test", "description": "Test"},
        headers=auth_headers
    )
    resource_id = create_response.json()["data"]["id"]
    
    # Get resource
    response = await client.get(
        f"/api/v1/resources/{resource_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == resource_id


@pytest.mark.asyncio
async def test_list_resources_pagination(client, auth_headers):
    """Test GET /api/v1/resources with pagination."""
    # Create multiple resources
    for i in range(15):
        await client.post(
            "/api/v1/resources",
            json={"name": f"Resource {i}", "description": "Test"},
            headers=auth_headers
        )
    
    # Get first page
    response = await client.get(
        "/api/v1/resources?skip=0&limit=10",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 10
    assert data["total"] == 15
    assert data["total_pages"] == 2
```

---

## 💾 CACHING PATTERNS

```python
"""
Caching patterns with Redis.
"""
from functools import wraps
from typing import Optional, Callable, Any
import json
import hashlib

from app.core.redis_client import redis_client
from app.config import settings


def cache_result(
    ttl: int = settings.cache_ttl_medium,
    key_prefix: str = "cache"
):
    """
    Decorator to cache function results in Redis.
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
    
    Usage:
        @cache_result(ttl=600, key_prefix="user")
        async def get_user(user_id: int) -> User:
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            key_data = {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs
            }
            key_hash = hashlib.md5(
                json.dumps(key_data, sort_keys=True).encode()
            ).hexdigest()
            cache_key = f"{key_prefix}:{key_hash}"
            
            # Try to get from cache
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Call function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await redis_client.set(
                cache_key,
                json.dumps(result),
                ttl=ttl
            )
            
            return result
        
        return wrapper
    return decorator


def invalidate_cache(key_pattern: str):
    """
    Invalidate cache by pattern.
    
    Args:
        key_pattern: Pattern to match keys (e.g., "user:*")
    """
    async def _invalidate():
        keys = await redis_client.redis.keys(key_pattern)
        if keys:
            await redis_client.redis.delete(*keys)
    
    return _invalidate
```

---

## 📡 EVENT-DRIVEN PATTERNS

```python
"""
Event publishing and consuming patterns.
"""
import json
from typing import Dict, Any, Callable, List
import aio_pika
import structlog

from app.config import settings

logger = structlog.get_logger()


class EventBus:
    """
    Event bus for publishing and consuming events.
    """
    
    def __init__(self):
        """Initialize event bus."""
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchange: Optional[aio_pika.Exchange] = None
        self.subscribers: Dict[str, List[Callable]] = {}
    
    async def connect(self):
        """Connect to RabbitMQ."""
        self.connection = await aio_pika.connect_robust(
            settings.rabbitmq_url
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            settings.rabbitmq_exchange,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        logger.info("eventbus_connected")
    
    async def disconnect(self):
        """Disconnect from RabbitMQ."""
        if self.connection:
            await self.connection.close()
        logger.info("eventbus_disconnected")
    
    async def publish(self, event_type: str, data: Dict[str, Any]):
        """
        Publish event.
        
        Args:
            event_type: Event type (e.g., "user.created")
            data: Event data
        """
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type="application/json"
        )
        
        await self.exchange.publish(
            message,
            routing_key=event_type
        )
        
        logger.info(
            "event_published",
            event_type=event_type,
            data=data
        )
    
    def subscribe(self, event_type: str):
        """
        Decorator to subscribe to events.
        
        Usage:
            @event_bus.subscribe("user.created")
            async def handle_user_created(event: dict):
                ...
        """
        def decorator(func: Callable):
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(func)
            return func
        return decorator
    
    async def start_consuming(self):
        """Start consuming events."""
        for event_type, handlers in self.subscribers.items():
            queue_name = f"{settings.rabbitmq_queue_prefix}.{event_type}"
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True
            )
            await queue.bind(self.exchange, routing_key=event_type)
            
            async def on_message(message: aio_pika.IncomingMessage):
                async with message.process():
                    data = json.loads(message.body.decode())
                    for handler in handlers:
                        try:
                            await handler(data)
                        except Exception as e:
                            logger.error(
                                "event_handler_error",
                                event_type=event_type,
                                error=str(e),
                                exc_info=True
                            )
            
            await queue.consume(on_message)
        
        logger.info(
            "eventbus_consuming",
            subscribed_events=list(self.subscribers.keys())
        )


# Global event bus
event_bus = EventBus()


# Usage example
@event_bus.subscribe("user.created")
async def handle_user_created(event: dict):
    """Handle user created event."""
    logger.info("handling_user_created", user_id=event["user_id"])
    # Send welcome email, create notifications, etc.
```

---

## 🔐 AUTHENTICATION PATTERNS

### JWT Authentication Dependency

```python
"""
JWT authentication patterns.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.services.user_service import UserService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
    
    Returns:
        Current user
    
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    service = UserService(db)
    user = await service.get_by_id(int(user_id))
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return current_user


def require_role(required_role: str):
    """
    Dependency to require specific role.
    
    Usage:
        @app.get("/admin")
        async def admin_route(user: User = Depends(require_role("admin"))):
            ...
    """
    async def _require_role(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required"
            )
        return current_user
    
    return _require_role
```

---

**See also:**
- `COMPLETE_ARCHITECTURE.md` - Full architecture guide
- `STANDARD_CONFIGURATIONS.md` - Configuration templates
- `TEAM_PROMPT.md` - Team standards

---

*Last Updated: November 10, 2025*  
*Maintained by: Gravity Elite Engineering Team*
