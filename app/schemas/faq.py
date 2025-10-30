from uuid import UUID

from pydantic import BaseModel


class FAQBase(BaseModel):
    question: str
    answer: str
    category: str | None = None
    display_order: int = 0
    is_active: bool = True


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    category: str | None = None
    display_order: int | None = None
    is_active: bool | None = None


class FAQResponse(FAQBase):
    id: UUID

    class Config:
        from_attributes = True
