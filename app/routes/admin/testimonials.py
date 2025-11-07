from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Testimonial
from app.schemas.testimonial import Testimonial as TestimonialSchema
from app.utils.auth import get_current_admin
from app.utils.image_processing import delete_gallery_image, save_gallery_image

router = APIRouter(prefix="/admin/testimonials", tags=["Testimonials"])


@router.get("/", response_model=List[TestimonialSchema])
@router.get("", response_model=List[TestimonialSchema])
async def get_testimonials(
    db: AsyncSession = Depends(get_db), current_admin=Depends(get_current_admin)
):
    result = await db.execute(select(Testimonial))
    testimonials = result.scalars().all()
    return testimonials


@router.post("/", response_model=TestimonialSchema)
@router.post("", response_model=TestimonialSchema)
async def create_testimonial(
    file: UploadFile | None = File(
        None, description="Upload testimonial image (optional)"
    ),
    name: str = Form(...),
    message: str = Form(...),
    rating: float = Form(...),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Create a testimonial with optional image upload.
    Image automatically generates an optimized thumbnail using Pillow.
    """
    image_url = None

    try:
        # Upload image if provided
        if file and file.filename:
            image_url, thumbnail_url = await save_gallery_image(file)

        # Create testimonial
        db_testimonial = Testimonial(
            name=name,
            message=message,
            image_url=image_url,
            rating=rating,
        )

        db.add(db_testimonial)
        await db.commit()
        await db.refresh(db_testimonial)

        return db_testimonial

    except ValueError as e:
        await db.rollback()
        # Clean up uploaded file if exists
        if image_url:
            try:
                delete_gallery_image(image_url, None)
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        # Clean up uploaded file if exists
        if image_url:
            try:
                delete_gallery_image(image_url, None)
            except Exception:
                pass
        raise HTTPException(
            status_code=500, detail=f"Failed to create testimonial: {str(e)}"
        )


@router.get("/{testimonial_id}", response_model=TestimonialSchema)
@router.get("/{testimonial_id}/", response_model=TestimonialSchema)
async def get_testimonial(
    testimonial_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    result = await db.execute(
        select(Testimonial).where(Testimonial.id == testimonial_id)
    )
    testimonial = result.scalar_one_or_none()
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return testimonial


@router.put("/{testimonial_id}", response_model=TestimonialSchema)
@router.put("/{testimonial_id}/", response_model=TestimonialSchema)
async def update_testimonial(
    testimonial_id: int,
    file: UploadFile | None = File(
        None, description="Upload new testimonial image (optional)"
    ),
    name: str | None = Form(None),
    message: str | None = Form(None),
    rating: float | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Update a testimonial.
    Optionally upload a new image (replaces existing).
    Only provided fields will be updated.
    """
    result = await db.execute(
        select(Testimonial).where(Testimonial.id == testimonial_id)
    )
    db_testimonial = result.scalar_one_or_none()
    if not db_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    old_image_url = None
    new_image_url = None

    try:
        # Upload new image if provided
        if file and file.filename:
            old_image_url = db_testimonial.image_url
            new_image_url, thumbnail_url = await save_gallery_image(file)
            db_testimonial.image_url = new_image_url

        # Update other fields
        if name is not None:
            db_testimonial.name = name
        if message is not None:
            db_testimonial.message = message
        if rating is not None:
            db_testimonial.rating = rating

        await db.commit()
        await db.refresh(db_testimonial)

        # Delete old image after successful update
        if old_image_url and new_image_url:
            try:
                delete_gallery_image(old_image_url, None)
            except Exception:
                pass

        return db_testimonial

    except ValueError as e:
        await db.rollback()
        # Clean up newly uploaded file if exists
        if new_image_url:
            try:
                delete_gallery_image(new_image_url, None)
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        # Clean up newly uploaded file if exists
        if new_image_url:
            try:
                delete_gallery_image(new_image_url, None)
            except Exception:
                pass
        raise HTTPException(
            status_code=500, detail=f"Failed to update testimonial: {str(e)}"
        )


@router.delete("/{testimonial_id}")
@router.delete("/{testimonial_id}/")
async def delete_testimonial(
    testimonial_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """
    Admin endpoint: Delete a testimonial and its associated image file.
    """
    result = await db.execute(
        select(Testimonial).where(Testimonial.id == testimonial_id)
    )
    testimonial = result.scalar_one_or_none()
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    # Delete image file if exists
    if testimonial.image_url:
        try:
            delete_gallery_image(testimonial.image_url, None)
        except Exception:
            # Continue even if file deletion fails
            pass

    await db.delete(testimonial)
    await db.commit()
    return {"message": "Testimonial deleted successfully"}
