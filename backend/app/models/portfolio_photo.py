# models/portfolio_photo.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class PortfolioPhoto(Base):
    __tablename__ = "portfolio_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("portfolio_items.item_id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255), nullable=False)

    item = relationship("PortfolioItem", back_populates="photos")
