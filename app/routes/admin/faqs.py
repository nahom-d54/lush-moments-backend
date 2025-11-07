from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import FAQ
from app.schemas.faq import FAQCreate, FAQResponse, FAQUpdate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/admin/faqs", tags=["Admin FAQs"])


@router.get("/", response_model=List[FAQResponse])
@router.get("", response_model=List[FAQResponse])
async def get_all_faqs(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Get all FAQs (including inactive)"""
    query = select(FAQ)

    if category:
        query = query.where(FAQ.category == category)

    query = query.order_by(FAQ.display_order, FAQ.question)

    result = await db.execute(query)
    faqs = result.scalars().all()
    return faqs


@router.get("/{faq_id}", response_model=FAQResponse)
@router.get("/{faq_id}/", response_model=FAQResponse)
async def get_faq(
    faq_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Get a specific FAQ by ID"""
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    return faq


@router.post("/", response_model=FAQResponse, status_code=201)
@router.post("", response_model=FAQResponse, status_code=201)
async def create_faq(
    faq_data: FAQCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Create a new FAQ"""
    faq = FAQ(**faq_data.model_dump())
    db.add(faq)
    await db.commit()
    await db.refresh(faq)
    return faq


@router.patch("/{faq_id}", response_model=FAQResponse)
@router.patch("/{faq_id}/", response_model=FAQResponse)
async def update_faq(
    faq_id: UUID,
    faq_data: FAQUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Update an existing FAQ"""
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    # Update only provided fields
    for key, value in faq_data.model_dump(exclude_unset=True).items():
        setattr(faq, key, value)

    await db.commit()
    await db.refresh(faq)
    return faq


@router.delete("/{faq_id}")
@router.delete("/{faq_id}/")
async def delete_faq(
    faq_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """Admin: Delete an FAQ"""
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await db.delete(faq)
    await db.commit()
    return {"message": "FAQ deleted successfully"}
