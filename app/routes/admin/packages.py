from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Package, PackageItem
from app.schemas.package import Package as PackageSchema
from app.schemas.package import PackageCreate, PackageUpdate
from app.utils.auth import get_current_admin
from app.utils.cache import clear_pattern

router = APIRouter(prefix="/admin/packages", tags=["admin packages"])


@router.get("/", response_model=List[PackageSchema])
async def get_packages(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .order_by(Package.display_order)
    )
    packages = result.scalars().all()
    return packages


@router.post("/", response_model=PackageSchema)
async def create_package(
    package: PackageCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    # Create package without items field
    package_data = package.model_dump(exclude={"items"})
    db_package = Package(**package_data)
    db.add(db_package)
    await db.flush()  # Get the package ID before adding items

    # Add package items
    for idx, item_text in enumerate(package.items):
        package_item = PackageItem(
            package_id=db_package.id,
            item_text=item_text,
            display_order=idx,
        )
        db.add(package_item)

    await db.commit()
    await db.refresh(db_package)

    # Reload with items
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .where(Package.id == db_package.id)
    )
    db_package = result.scalar_one()

    # Clear cache
    await clear_pattern("packages:*")

    return db_package


@router.get("/{package_id}", response_model=PackageSchema)
async def get_package(
    package_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .where(Package.id == package_id)
    )
    package = result.scalar_one_or_none()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


@router.patch("/{package_id}", response_model=PackageSchema)
async def update_package(
    package_id: int,
    package: PackageUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .where(Package.id == package_id)
    )
    db_package = result.scalar_one_or_none()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Update package fields
    update_data = package.model_dump(exclude_unset=True, exclude={"items"})
    for key, value in update_data.items():
        setattr(db_package, key, value)

    # Update items if provided
    if package.items is not None:
        # Delete existing items
        for item in db_package.items:
            await db.delete(item)

        # Add new items
        for idx, item_text in enumerate(package.items):
            package_item = PackageItem(
                package_id=db_package.id,
                item_text=item_text,
                display_order=idx,
            )
            db.add(package_item)

    await db.commit()
    await db.refresh(db_package)

    # Reload with items
    result = await db.execute(
        select(Package)
        .options(selectinload(Package.items))
        .where(Package.id == db_package.id)
    )
    db_package = result.scalar_one()

    # Clear cache
    await clear_pattern("packages:*")

    return db_package


@router.delete("/{package_id}")
async def delete_package(
    package_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(select(Package).where(Package.id == package_id))
    package = result.scalar_one_or_none()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    await db.delete(package)
    await db.commit()

    # Clear cache
    await clear_pattern("packages:*")

    return {"message": "Package deleted successfully"}
