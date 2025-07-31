# models/portfolio_item.py
from sqlalchemy import Column, Integer, Text, Enum, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from models.base import Base
from models.portfolio_photo import PortfolioPhoto
from .specialization import SpecializationTypeEnum

class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    item_id = Column(Integer, primary_key=True, index=True)
    photographer_id = Column(Integer, ForeignKey("photographers.photographer_id"), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(ENUM(SpecializationTypeEnum), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    photographer = relationship("Photographer", back_populates="portfolio_items")
    photos = relationship("PortfolioPhoto", back_populates="item", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_portfolio_photographer', 'photographer_id'),
        Index('idx_portfolio_category', 'category'),
    )
