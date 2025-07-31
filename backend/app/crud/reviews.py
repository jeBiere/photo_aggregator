from sqlalchemy.orm import Session
from models.reviews import Review
from schemas.reviews import ReviewCreate, ReviewUpdate
from datetime import datetime

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.review_id == review_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Review).offset(skip).limit(limit).all()

def get_reviews_by_user(db: Session, user_id: int):
    return db.query(Review).filter(Review.user_id == user_id).all()

def get_reviews_for_photographer(db: Session, photographer_id: int):
    return db.query(Review).filter(Review.photographer_id == photographer_id).all()

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, updates: ReviewUpdate):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()
    if db_review:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_review, field, value)
        db_review.created_at = datetime.utcnow()
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.review_id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review
