from sqlalchemy import Column, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    login = Column(String, primary_key=True)  # Логин остаётся первичным ключом
    hashed_password = Column(String, nullable=False)  # Теперь пароль хранится в хеше
    email = Column(String, nullable=False, unique=True)  # Email теперь уникальный и обязательный
    registration_date = Column(DateTime)  # Дата регистрации
    is_active = Column(Boolean, default=True)  # Флаг активности пользователя

    __table_args__ = (UniqueConstraint('email', name='unique_email'),)  # Уникальность email

