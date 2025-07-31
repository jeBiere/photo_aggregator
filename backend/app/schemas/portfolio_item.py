# schemas/portfolio_item.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.portfolio_photo import PortfolioPhotoInDB
from models.specialization import SpecializationTypeEnum

class PortfolioItemBase(BaseModel):
    description: Optional[str] = None
    category: Optional[SpecializationTypeEnum] = None

class PortfolioItemCreate(PortfolioItemBase):
    pass

class PortfolioItemUpdate(PortfolioItemBase):
    pass

class PortfolioItemInDB(PortfolioItemBase):
    item_id: int
    photographer_id: int
    created_at: datetime
    photos: List[PortfolioPhotoInDB] = []

    class Config:
        orm_mode = True
