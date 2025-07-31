from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import condecimal

# Схема для базового представления фотостудии
class PhotoStudioBase(BaseModel):
    studio_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website_url: Optional[HttpUrl] = None
    profile_picture_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = True
    base_price_per_hour: condecimal(max_digits=10, decimal_places=2)


    class Config:
        orm_mode = True

# Схема для создания новой фотостудии
class PhotoStudioCreate(PhotoStudioBase):
    pass  

class PhotoStudioUpdate(PhotoStudioBase):
    pass

# Схема для вывода данных о фотостудии (например, в ответах API)
class PhotoStudioInDB(PhotoStudioBase):
    studio_id: int
    created_at: datetime

    class Config:
        orm_mode = True
