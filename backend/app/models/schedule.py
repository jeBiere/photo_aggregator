from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base

class WorkingHoursTemplate(Base):
    __tablename__ = "working_hours_template"
    id = Column(Integer, primary_key=True)
    photographer_id = Column(Integer, ForeignKey("photographers.photographer_id", ondelete="CASCADE"))
    day_of_week = Column(SmallInteger, nullable=False)  # 0 = Monday, 6 = Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

class BlockedSlot(Base):
    __tablename__ = "blocked_slots"
    id = Column(Integer, primary_key=True)
    photographer_id = Column(Integer, ForeignKey("photographers.photographer_id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)  # NULL = весь день
    end_time = Column(Time, nullable=True)
    reason = Column(Text)