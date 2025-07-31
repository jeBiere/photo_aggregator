from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Схема для базового представления отзыва
class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

    class Config:
        orm_mode = True

# Схема для создания отзыва
class ReviewCreate(ReviewBase):
    order_id: int
    photographer_id: int
    user_id: int

# Схема для вывода данных о отзыве
class ReviewInDB(ReviewBase):
    review_id: int
    order_id: int
    photographer_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

    class Config:
        orm_mode = True