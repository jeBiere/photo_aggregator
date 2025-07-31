from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.reviews import ReviewCreate, ReviewUpdate, ReviewInDB
from models.user import User, UserRole
from models.photographer import Photographer
from crud import reviews as crud_review
from db import get_db
from utils.jwt_utils import get_current_user

router = APIRouter()

@router.post("/", response_model=ReviewInDB)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = crud_review.create_review(db, review)
    
    # Вручную преобразуем в dict, затем валидируем
    review_data = {
        "review_id": db_review.review_id,
        "order_id": db_review.order_id,
        "photographer_id": db_review.photographer_id,
        "user_id": db_review.user_id,
        "rating": db_review.rating,
        "comment": db_review.comment,
        "created_at": db_review.created_at
    }
    
    return ReviewInDB.parse_obj(review_data)  # ← Явная валидация

@router.get("/", response_model=List[ReviewInDB])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_review.get_reviews(db, skip=skip, limit=limit)

@router.get("/me", response_model=List[ReviewInDB])
async def get_my_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.client:
        return crud_review.get_reviews_by_user(db, current_user.user_id)

    elif current_user.role == UserRole.photographer or current_user.role == UserRole.admin:
        photographer = db.query(Photographer).filter(
            Photographer.user_id == current_user.user_id
        ).first()

        if not photographer:
            raise HTTPException(status_code=404, detail="Photographer profile not found")

        return crud_review.get_reviews_for_photographer(db, photographer.photographer_id)

    else:
        raise HTTPException(status_code=403, detail=f"Unsupported role {current_user.role}!")
    
@router.get("/{review_id}", response_model=ReviewInDB)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud_review.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.put("/{review_id}", response_model=ReviewInDB)
def update_review(review_id: int, updates: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud_review.update_review(db, review_id, updates)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.delete("/{review_id}", response_model=ReviewInDB)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud_review.delete_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review
