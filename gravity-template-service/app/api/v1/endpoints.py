"""
Example API Endpoints
Replace this with your actual endpoints
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.logging_config import logger
from app.dependencies import PaginationParams, get_current_user, get_pagination_params
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleResponse, ExampleUpdate
from app.schemas.response import PaginatedResponse

# Create router
example_router = APIRouter()


@example_router.get("/", response_model=PaginatedResponse[ExampleResponse])
async def list_examples(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
):
    """
    List all examples with pagination

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    logger.info("Listing examples", skip=pagination.skip, limit=pagination.limit)

    # Count total
    count_query = select(Example)
    total_result = await db.execute(count_query)
    total = len(total_result.scalars().all())

    # Get items
    query = select(Example).offset(pagination.skip).limit(pagination.limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }


@example_router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(
    example_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific example by ID

    - **example_id**: The ID of the example to retrieve
    """
    logger.info("Getting example", example_id=example_id)

    result = await db.execute(select(Example).where(Example.id == example_id))
    example = result.scalar_one_or_none()

    if not example:
        logger.warning("Example not found", example_id=example_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )

    return example


@example_router.post(
    "/",
    response_model=ExampleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_example(
    example_data: ExampleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new example

    Requires authentication.
    """
    logger.info("Creating example", user_id=current_user.get("sub"))

    example = Example(**example_data.model_dump())
    db.add(example)
    await db.commit()
    await db.refresh(example)

    logger.info("Example created", example_id=example.id)

    return example


@example_router.put("/{example_id}", response_model=ExampleResponse)
async def update_example(
    example_id: int,
    example_data: ExampleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update an existing example

    Requires authentication.
    """
    logger.info("Updating example", example_id=example_id, user_id=current_user.get("sub"))

    result = await db.execute(select(Example).where(Example.id == example_id))
    example = result.scalar_one_or_none()

    if not example:
        logger.warning("Example not found for update", example_id=example_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )

    # Update fields
    for field, value in example_data.model_dump(exclude_unset=True).items():
        setattr(example, field, value)

    await db.commit()
    await db.refresh(example)

    logger.info("Example updated", example_id=example.id)

    return example


@example_router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(
    example_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete an example

    Requires authentication.
    """
    logger.info("Deleting example", example_id=example_id, user_id=current_user.get("sub"))

    result = await db.execute(select(Example).where(Example.id == example_id))
    example = result.scalar_one_or_none()

    if not example:
        logger.warning("Example not found for deletion", example_id=example_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found",
        )

    await db.delete(example)
    await db.commit()

    logger.info("Example deleted", example_id=example_id)

    return None
