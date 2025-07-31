from sqlalchemy import Column, Integer, Enum, ForeignKey, Index
from sqlalchemy.orm import relationship
from models.base import Base
import enum


class SpecializationTypeEnum(str, enum.Enum):
    portrait = "portrait"
    wedding = "wedding"
    family = "family"
    children = "children"
    event = "event"
    fashion = "fashion"
    boudoir = "boudoir"
    sports = "sports"
    studio = "studio"
    on_location = "on_location"
    product = "product"
    love_story = "love_story"


class PhotographerSpecialization(Base):
    __tablename__ = "photographer_specializations"

    photographer_id = Column(
        Integer,
        ForeignKey("photographers.photographer_id", ondelete="CASCADE"),
        primary_key=True
    )
    specialization = Column(
        Enum(SpecializationTypeEnum, name="specialization_type"),
        nullable=False,
        primary_key=True
    )

    __table_args__ = (
        Index("idx_specializations_type", "specialization"),
    )
