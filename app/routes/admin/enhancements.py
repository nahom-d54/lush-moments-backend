from typing import List
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
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/enhancements", tags=["Admin Package Enhancements"])


@router.get("/", response_model=List[PackageEnhancementResponse])
@router.get("", response_model=List[PackageEnhancementResponse])
async def get_all_enhancements(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Get all package enhancements (including unavailable)"""
    query = select(PackageEnhancement)

    if category:
        query = query.where(PackageEnhancement.category == category)

    query = query.order_by(PackageEnhancement.display_order, PackageEnhancement.name)

    result = await db.execute(query)
    enhancements = result.scalars().all()
    return enhancements


@router.get("/{enhancement_id}", response_model=PackageEnhancementResponse)
@router.get("/{enhancement_id}/", response_model=PackageEnhancementResponse)
async def get_enhancement(
    enhancement_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Get a specific enhancement by ID"""
    result = await db.execute(
        select(PackageEnhancement).where(PackageEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()

    if not enhancement:
        raise HTTPException(status_code=404, detail="Enhancement not found")

    return enhancement


@router.post("/", response_model=PackageEnhancementResponse, status_code=201)
@router.post("", response_model=PackageEnhancementResponse, status_code=201)
async def create_enhancement(
    enhancement_data: PackageEnhancementCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Create a new package enhancement"""
    enhancement = PackageEnhancement(**enhancement_data.model_dump())
    db.add(enhancement)
    await db.commit()
    await db.refresh(enhancement)
    return enhancement


@router.patch("/{enhancement_id}", response_model=PackageEnhancementResponse)
@router.patch("/{enhancement_id}/", response_model=PackageEnhancementResponse)
async def update_enhancement(
    enhancement_id: UUID,
    enhancement_data: PackageEnhancementUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Update an existing package enhancement"""
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


@router.delete("/{enhancement_id}")
@router.delete("/{enhancement_id}/")
async def delete_enhancement(
    enhancement_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Delete a package enhancement"""
    result = await db.execute(
        select(PackageEnhancement).where(PackageEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()

    if not enhancement:
        raise HTTPException(status_code=404, detail="Enhancement not found")

    await db.delete(enhancement)
    await db.commit()
    return {"message": "Enhancement deleted successfully"}
