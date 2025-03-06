from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Базовая схема (общая для других)
class UserBase(BaseModel):
    login: str
    email: EmailStr
    is_active: bool = True  # Флаг активности пользователя
    registration_date: datetime

# Схема для создания нового пользователя (при регистрации)
class UserCreate(BaseModel):
    login: str
    email: EmailStr
    password: str  # Передаётся в открытом виде, будет хешироваться
    registration_date: datetime = Field(default_factory=datetime.now)

# Схема для обновления пользователя (например, смена email или пароля)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Схема для входа в систему
class UserLogin(BaseModel):
    login: str = Field(..., alias="username")
    password: str

    class Config:
        allow_population_by_field_name = True

# Схема пользователя, который хранится в БД (с уже хешированным паролем)
class UserInDB(UserBase):
    hashed_password: str  # Показываем уже хешированный пароль

    class Config:
        orm_mode = True
        from_attributes = True
