from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, TIMESTAMP, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.base import Base

class PhotoStudio(Base):
    __tablename__ = "photo_studios"

    studio_id = Column(Integer, primary_key=True, autoincrement=True)
    studio_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website_url = Column(String(255), nullable=True)
    profile_picture_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    base_price_per_hour = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())


    orders = relationship("Order", backref="studio", lazy="dynamic")
    photos = relationship("StudioPhoto", back_populates="studio", cascade="all, delete-orphan")
    
    # Индексы
    __table_args__ = (
        Index('idx_studio_name', 'studio_name'),
        Index('idx_studio_email', 'email'),
        Index('idx_studio_phone', 'phone')
    )
