from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint
from models.base import Base 

class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), unique=True, nullable=False)
    photographer_id = Column(Integer, ForeignKey("photographers.photographer_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('order_id', name='unique_order_review'), 
        Index('idx_reviews_photographer', 'photographer_id'),
        Index('idx_reviews_user', 'user_id')
    )
    order = relationship("Order", backref="reviews")
    photographer = relationship("Photographer", backref="reviews")
    user = relationship("User", backref="reviews")
