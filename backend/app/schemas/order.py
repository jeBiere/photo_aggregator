from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import date, time, datetime
from enum import Enum


class OrderStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


# 🔹 Общая базовая схема
class OrderBase(BaseModel):
    user_id: int
    photographer_id: Optional[int] = None
    studio_id: Optional[int] = None 
    status: OrderStatusEnum = OrderStatusEnum.pending
    shoot_date: date
    start_time: time
    duration: int
    price: condecimal(max_digits=10, decimal_places=2)
    address: Optional[str] = None
    special_requests: Optional[str] = None


# 🔹 Схема создания заказа
class OrderCreate(OrderBase):
    pass


# 🔹 Схема обновления заказа
class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    shoot_date: Optional[date] = None
    start_time: Optional[time] = None
    duration: Optional[int] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    address: Optional[str] = None
    special_requests: Optional[str] = None


# 🔹 Схема возвращаемого заказа (например, в ответе API)
class OrderInDB(OrderBase):
    order_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
