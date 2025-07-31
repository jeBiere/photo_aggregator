from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from datetime import datetime
from models.base import Base

# Перечисление ролей пользователя для SQLAlchemy
class UserRole(PyEnum):
    client = "client"
    photographer = "photographer"
    admin = "admin"

# Модель пользователя
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор пользователя
    first_name = Column(String(100), nullable=False)  # Имя пользователя
    last_name = Column(String(100), nullable=False)  # Фамилия пользователя
    login = Column(String(100), unique=True, nullable=False)  # Логин для авторизации
    email = Column(String(255), unique=True, nullable=False)  # Электронная почта
    phone = Column(String(20), nullable=True)  # Телефон (опционально)
    city = Column(String(255), nullable=False)  # Город проживания
    password_hash = Column(String(255), nullable=False)  # Хешированный пароль
    avatar_url = Column(String(255), nullable=True)  # Путь к изображению (опционально)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # Дата создания
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата последнего обновления
    status = Column(String(50), default="active")  # Статус пользователя
    role = Column(Enum(UserRole), default=UserRole.client)  # Роль пользователя (ENUM)

    # Индексы для ускорения поиска
    __table_args__ = (
        Index('idx_user_email', email),  # Индекс на поле email
        Index('idx_user_phone', phone),  # Индекс на поле phone
        Index('idx_user_role', role)     # Индекс на поле role
    )

    # Если нужно, можно добавить отношения, например, для связи с заказами или отзывами

    # Например, связь с таблицей отзывов:
    #orders = relationship("Order", backref="user.user_id")