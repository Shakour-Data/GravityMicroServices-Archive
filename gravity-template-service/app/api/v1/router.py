"""
API v1 Router
Aggregates all API endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import example_router

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(example_router, prefix="/examples", tags=["Examples"])

# Add more routers here as needed
# api_router.include_router(users_router, prefix="/users", tags=["Users"])
# api_router.include_router(items_router, prefix="/items", tags=["Items"])
