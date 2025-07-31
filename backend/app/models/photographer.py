from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from models.base import Base

# Модель фотографа
class Photographer(Base):
    __tablename__ = 'photographers'

    photographer_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False) 
    description = Column(Text, nullable=True) 
    experience_years = Column(Integer, nullable=True) 
    city = Column(String(100), nullable=False) 
    rating = Column(Numeric(3, 2), default=0.00, nullable=True) 
    is_active = Column(Boolean, default=True)  
    price_per_hour = Column(Numeric(10, 2), nullable=True) 

    user = relationship('User', backref='photographers')
    portfolio_items = relationship("PortfolioItem", back_populates="photographer")

    __table_args__ = (
        Index('idx_photographers_city', city),
        Index('idx_photographers_rating', rating),
    )
