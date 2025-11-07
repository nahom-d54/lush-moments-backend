from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import FAQ
from app.schemas.faq import FAQResponse

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.get("", response_model=list[FAQResponse])
@router.get("/", response_model=list[FAQResponse])
async def get_faqs(
    category: str | None = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """Get all active FAQs, optionally filtered by category"""
    query = select(FAQ)

    if active_only:
        query = query.where(FAQ.is_active == True)

    if category:
        query = query.where(FAQ.category == category)

    query = query.order_by(FAQ.display_order, FAQ.question)

    result = await db.execute(query)
    faqs = result.scalars().all()
    return faqs


@router.get("/categories/")
@router.get("/categories")
async def get_faq_categories(db: AsyncSession = Depends(get_db)):
    """Get all unique FAQ categories"""
    result = await db.execute(
        select(FAQ.category).where(FAQ.category.isnot(None)).distinct()
    )
    categories = result.scalars().all()
    return {"categories": categories}


@router.get("/{faq_id}/", response_model=FAQResponse)
@router.get("/{faq_id}", response_model=FAQResponse)
async def get_faq(faq_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific FAQ by ID"""
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    return faq
