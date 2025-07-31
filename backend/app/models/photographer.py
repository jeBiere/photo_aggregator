from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from models.base import Base

# Модель фотографа
class Photographer(Base):
    __tablename__ = 'photographers'

    photographer_id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор фотографа
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)  # Ссылка на пользователя
    description = Column(Text, nullable=True)  # Описание
    experience_years = Column(Integer, nullable=True)  # Стаж (лет)
    city = Column(String(100), nullable=False)  # Город для поиска
    rating = Column(Numeric(3, 2), default=0.00, nullable=True)  # Средний рейтинг
    is_active = Column(Boolean, default=True)  # Активен ли профиль
    price_per_hour = Column(Numeric(10, 2), nullable=True)  # Ставка (руб/час)

    # Связь с таблицей пользователей
    user = relationship('User', backref='photographers')
    portfolio_items = relationship("PortfolioItem", back_populates="photographer")

    # Индексы для ускорения поиска
    __table_args__ = (
        Index('idx_photographers_city', city),  # Индекс на поле city
        Index('idx_photographers_rating', rating),  # Индекс на поле rating
    )
