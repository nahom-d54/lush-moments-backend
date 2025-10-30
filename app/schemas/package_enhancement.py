from uuid import UUID

from pydantic import BaseModel


class PackageEnhancementBase(BaseModel):
    name: str
    description: str
    starting_price: float
    category: str | None = None
    icon: str | None = None
    is_available: bool = True
    display_order: int = 0


class PackageEnhancementCreate(PackageEnhancementBase):
    pass


class PackageEnhancementUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    starting_price: float | None = None
    category: str | None = None
    icon: str | None = None
    is_available: bool | None = None
    display_order: int | None = None


class PackageEnhancementResponse(PackageEnhancementBase):
    id: UUID

    class Config:
        from_attributes = True
