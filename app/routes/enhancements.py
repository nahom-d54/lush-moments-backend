from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import PackageEnhancement
from app.schemas.package_enhancement import PackageEnhancementResponse

router = APIRouter(prefix="/enhancements", tags=["Package Enhancements"])


@router.get("", response_model=list[PackageEnhancementResponse])
@router.get("/", response_model=list[PackageEnhancementResponse])
async def get_enhancements(
    category: str | None = None,
    available_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """Get all available package enhancements, optionally filtered by category"""
    query = select(PackageEnhancement)

    if available_only:
        query = query.where(PackageEnhancement.is_available.is_(True))

    if category:
        query = query.where(PackageEnhancement.category == category)

    query = query.order_by(PackageEnhancement.display_order, PackageEnhancement.name)

    result = await db.execute(query)
    enhancements = result.scalars().all()
    return enhancements


@router.get("/categories/")
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


@router.get("/{enhancement_id}/", response_model=PackageEnhancementResponse)
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
