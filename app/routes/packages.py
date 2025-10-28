from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Package, PackageItem
from app.schemas.package import (
    Package as PackageSchema,
)
from app.schemas.package import (
    PackageCreate,
    PackageUpdate,
)
from app.utils.cache import get_cached, set_cached
from app.utils.translations import apply_translations

router = APIRouter(prefix="/packages", tags=["Packages"])


@router.get("/", response_model=List[PackageSchema])
async def get_packages(
    db: AsyncSession = Depends(get_db),
    lang: Optional[str] = Query(
        "en", description="Language code (e.g., 'en', 'es', 'fr')"
    ),
):
    # Try to get from cache
    cache_key = f"packages:{lang}"
    cached_data = await get_cached(cache_key)
    if cached_data:
        return cached_data

    # Fetch packages with their items
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .order_by(Package.display_order)
    )
    packages = result.scalars().all()

    # Apply translations if language is not English
    if lang != "en":
        translated_packages = []
        for package in packages:
            translated_package = await apply_translations(db, package, "Package", lang)
            translated_packages.append(translated_package)

        # Convert to dict for caching
        packages_dict = [
            PackageSchema.model_validate(p).model_dump() for p in translated_packages
        ]
        await set_cached(cache_key, packages_dict, expire=600)
        return translated_packages

    # Convert to dict for caching
    packages_dict = [PackageSchema.model_validate(p).model_dump() for p in packages]
    await set_cached(cache_key, packages_dict, expire=600)
    return packages


@router.get("/{package_id}", response_model=PackageSchema)
async def get_package(
    package_id: int,
    db: AsyncSession = Depends(get_db),
    lang: Optional[str] = Query("en", description="Language code"),
):
    """Get a specific package by ID with its items"""
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .where(Package.id == package_id)
    )
    package = result.scalar_one_or_none()

    if not package:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Package not found")

    # Apply translations if needed
    if lang != "en":
        package = await apply_translations(db, package, "Package", lang)

    return package
