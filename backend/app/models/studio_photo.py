# models/studio_photo.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class StudioPhoto(Base):
    __tablename__ = "studio_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    studio_id = Column(Integer, ForeignKey("photo_studios.studio_id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255), nullable=False)

    studio = relationship("PhotoStudio", back_populates="photos")
