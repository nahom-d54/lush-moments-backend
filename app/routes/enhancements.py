from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import PackageEnhancement
from app.schemas.package_enhancement import (
    PackageEnhancementCreate,
    PackageEnhancementResponse,
    PackageEnhancementUpdate,
)

router = APIRouter(prefix="/enhancements", tags=["Package Enhancements"])


@router.get("/", response_model=list[PackageEnhancementResponse])
async def get_enhancements(
    category: str | None = None,
    available_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """Get all package enhancements, optionally filtered by category"""
    query = select(PackageEnhancement)

    if available_only:
        query = query.where(PackageEnhancement.is_available.is_(True))

    if category:
        query = query.where(PackageEnhancement.category == category)

    query = query.order_by(PackageEnhancement.display_order, PackageEnhancement.name)

    result = await db.execute(query)
    enhancements = result.scalars().all()
    return enhancements


@router.get("/categories")
async def get_enhancement_categories(db: AsyncSession = Depends(get_db)):
    """Get all unique enhancement categories"""
    result = await db.execute(
        select(PackageEnhancement.category)
        .where(PackageEnhancement.category.isnot(None))
        .distinct()
    )
    categories = result.scalars().all()
    return {"categories": categories}


@router.get("/{enhancement_id}", response_model=PackageEnhancementResponse)
async def get_enhancement(enhancement_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific enhancement by ID"""
    result = await db.execute(
        select(PackageEnhancement).where(PackageEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()

    if not enhancement:
        raise HTTPException(status_code=404, detail="Enhancement not found")

    return enhancement


@router.post("/", response_model=PackageEnhancementResponse, status_code=201)
async def create_enhancement(
    enhancement_data: PackageEnhancementCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new package enhancement"""
    enhancement = PackageEnhancement(**enhancement_data.model_dump())
    db.add(enhancement)
    await db.commit()
    await db.refresh(enhancement)
    return enhancement


@router.put("/{enhancement_id}", response_model=PackageEnhancementResponse)
async def update_enhancement(
    enhancement_id: UUID,
    enhancement_data: PackageEnhancementUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing package enhancement"""
    result = await db.execute(
        select(PackageEnhancement).where(PackageEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()

    if not enhancement:
        raise HTTPException(status_code=404, detail="Enhancement not found")

    # Update only provided fields
    for key, value in enhancement_data.model_dump(exclude_unset=True).items():
        setattr(enhancement, key, value)

    await db.commit()
    await db.refresh(enhancement)
    return enhancement


@router.delete("/{enhancement_id}", status_code=204)
async def delete_enhancement(enhancement_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a package enhancement"""
    result = await db.execute(
        select(PackageEnhancement).where(PackageEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()

    if not enhancement:
        raise HTTPException(status_code=404, detail="Enhancement not found")

    await db.delete(enhancement)
    await db.commit()
    return None
