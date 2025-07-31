from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

# Перечисление ролей пользователя
class UserRole(str, Enum):
    client = "client"
    photographer = "photographer"
    admin = "admin"

# Базовая схема пользователя (общая)
class UserBase(BaseModel):
    first_name: str
    last_name: str
    login: str
    email: EmailStr
    phone: Optional[str] = None
    city: str
    avatar_url: Optional[str] = None
    status: str = "active"
    role: UserRole = UserRole.client  # Используем перечисление для роли

# Схема для создания пользователя (регистрация)
class UserCreate(UserBase):
    password: str  # Передается открытым текстом, будет хешироваться

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None

# Схема пользователя, хранящегося в БД
class UserInDB(UserBase):
    user_id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime
  
    class Config:
        orm_mode = True
        from_attributes = True

# Схема для логина пользователя
class UserLogin(BaseModel):
    login: str  # Логин
    password: str  # Пароль (в открытом виде)

    class Config:
        orm_mode = True