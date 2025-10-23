from typing import List, Optional

from pydantic import BaseModel


class PackageItemBase(BaseModel):
    item_text: str
    display_order: int = 0


class PackageItemCreate(PackageItemBase):
    pass


class PackageItem(PackageItemBase):
    id: int
    package_id: int

    class Config:
        from_attributes = True


class PackageBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    is_popular: bool = False
    display_order: int = 0


class PackageCreate(PackageBase):
    items: List[str]  # List of bullet point strings


class PackageUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_popular: Optional[bool] = None
    display_order: Optional[int] = None
    items: Optional[List[str]] = None


class Package(PackageBase):
    id: int
    items: List[PackageItem] = []

    class Config:
        from_attributes = True


class PackageWithDetails(Package):
    """Package with all details for frontend display"""

    pass
