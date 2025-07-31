from sqlalchemy import (Column,Integer,String,Text,Date,Time,Numeric,Enum,ForeignKey,TIMESTAMP, Index)
from sqlalchemy.orm import declarative_base, relationship
import enum
from models.base import Base
from datetime import datetime



class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    photographer_id = Column(Integer, ForeignKey("photographers.photographer_id", ondelete="SET NULL"), nullable=True)
    studio_id = Column(Integer, ForeignKey("photo_studios.studio_id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(OrderStatusEnum, name="order_status"), nullable=False, default=OrderStatusEnum.pending)
    shoot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False, default=1)  
    price = Column(Numeric(10, 2), nullable=False)
    address = Column(Text)
    special_requests = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", backref="orders")
    photographer = relationship("Photographer", backref="orders")


    __table_args__ = (
        Index("idx_orders_client", "user_id"),
        Index("idx_orders_photographer", "photographer_id"),
        Index("idx_orders_date", "shoot_date"),
    )