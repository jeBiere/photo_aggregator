from pydantic import BaseModel, condecimal, conint, confloat
from typing import Optional, List
from datetime import datetime
from models.specialization import SpecializationTypeEnum


class PhotographerBase(BaseModel):
    description: Optional[str] = None  # Описание (не обязательно)
    experience_years: Optional[conint(ge=0)] = None  # Стаж (лет), не может быть отрицательным
    rating: Optional[condecimal(ge=0, le=5, max_digits=3, decimal_places=2)] = 0.00  # Рейтинг от 0 до 5
    is_active: Optional[bool] = True  # Активен ли профиль
    price_per_hour: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # Ставка (руб/час)
    city : Optional[str] = None

    class Config:
        orm_mode = True


class PhotographerCreate(PhotographerBase):
    user_id: int  # ID пользователя, который будет связан с фотографом


class PhotographerUpdate(BaseModel):
    description: Optional[str] = None
    experience_years: Optional[conint(ge=0)] = None
    rating: Optional[condecimal(ge=0, le=5, max_digits=3, decimal_places=2)] = None
    is_active: Optional[bool] = None
    price_per_hour: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    city : Optional[str] = None


class PhotographerInDB(PhotographerBase):
    photographer_id: int  # Уникальный идентификатор фотографа
    user_id: int  # ID пользователя, который связан с фотографом

    class Config:
        orm_mode = True  # Указывает на использование ORM модели при ответах API
        from_attributes = True

class PhotographerFilterParams(BaseModel):
    city: Optional[str] = None
    specializations: Optional[List[SpecializationTypeEnum]] = None
    max_price: Optional[float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "city": "Москва",
                "specializations": ["wedding", "portrait"],
                "max_price": 15000
            }
        }

class PhotographerRelevanceParams(BaseModel):
    rating_weight: Optional[confloat(ge=0, le=1)] = 0.5
    orders_weight: Optional[confloat(ge=0, le=1)] = 0.3
    reviews_weight: Optional[confloat(ge=0, le=1)] = 0.2
    
    class Config:
        schema_extra = {
            "example": {
                "rating_weight": 0.6,
                "orders_weight": 0.25,
                "reviews_count": 0.15
            }
        }