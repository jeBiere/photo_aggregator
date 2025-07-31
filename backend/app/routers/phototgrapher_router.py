from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.photographer import PhotographerCreate, PhotographerUpdate, PhotographerInDB, PhotographerFilterParams, PhotographerRelevanceParams
from models.specialization import SpecializationTypeEnum
from models.photographer import Photographer
from schemas.order import OrderInDB
from schemas.reviews import ReviewInDB
from schemas.portfolio_item import PortfolioItemInDB
from crud import photographer as crud_photographer
from db import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=PhotographerInDB)
def create_photographer(photographer: PhotographerCreate, db: Session = Depends(get_db)):
    return crud_photographer.create_photographer(db, photographer)

@router.get("/", response_model=List[PhotographerInDB])
def read_photographers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_photographer.get_photographers(db, skip=skip, limit=limit)

@router.post("/filter/", response_model=List[PhotographerInDB])
def filter_photographers(
    filters: PhotographerFilterParams,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    photographers = crud_photographer.get_filtered_photographers(
        db,
        city=filters.city,
        specializations=filters.specializations,
        max_price=filters.max_price
    )
    return photographers[skip:skip+limit]  # Пагинация

@router.post("/recommendations/", response_model=List[PhotographerInDB])
def get_relevant_photographers(
    filters: PhotographerFilterParams,
    relevance: PhotographerRelevanceParams = Depends(),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получение фотографов с учётом:
    1. Жёстких фильтров (город, специализации, цена)
    2. Сортировки по взвешенному рейтингу
    """
    # Фильтрация
    photographers = crud_photographer.get_filtered_photographers(
        db,
        city=filters.city,
        specializations=filters.specializations,
        max_price=filters.max_price
    )
    
    # Сортировка по релевантности
    sorted_photographers = crud_photographer.get_sorted_by_relevance(
        db,
        photographers=photographers,
        rating_weight=relevance.rating_weight,
        orders_weight=relevance.orders_weight,
        reviews_weight=relevance.reviews_weight
    )
    
    return sorted_photographers[skip:skip+limit]

@router.get("/orders", response_model=List[OrderInDB])
def read_user_orders(
    photographer_id: int,
    db: Session = Depends(get_db)
):
    # Проверка существования пользователя может быть здесь или в CRUD
    if not db.query(Photographer).filter(Photographer.photographer_id == photographer_id).first():
        raise HTTPException(status_code=404, detail="Photographer not found")
    
    return crud_photographer.get_photographer_orders(db, photographer_id=photographer_id)


@router.get("/{photographer_id}", response_model=PhotographerInDB)
def read_photographer(photographer_id: int, db: Session = Depends(get_db)):
    db_photographer = crud_photographer.get_photographer(db, photographer_id)
    if db_photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return db_photographer

@router.put("/{photographer_id}", response_model=PhotographerInDB)
def update_photographer(photographer_id: int, updates: PhotographerUpdate, db: Session = Depends(get_db)):
    db_photographer = crud_photographer.update_photographer(db, photographer_id, updates)
    if db_photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return db_photographer

@router.delete("/{photographer_id}", response_model=PhotographerInDB)
def delete_photographer(photographer_id: int, db: Session = Depends(get_db)):
    db_photographer = crud_photographer.delete_photographer(db, photographer_id)
    if db_photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return db_photographer

@router.get("/{photographer_id}/specializations/", response_model=List[SpecializationTypeEnum])
def read_specializations(
    photographer_id: int,
    db: Session = Depends(get_db)
):
    return crud_photographer.get_photographer_specializations(db, photographer_id)

@router.get("/{photographer_id}/reviews/", response_model=List[ReviewInDB])
def read_reviews(
    photographer_id: int,
    db: Session = Depends(get_db)
):
    return crud_photographer.get_photographer_reviews(db, photographer_id)

@router.get("/{photographer_id}/portfolio/", response_model=List[PortfolioItemInDB])
def read_portfolio(
    photographer_id: int,
    db: Session = Depends(get_db)
):
    return crud_photographer.get_photographer_portfolio(db, photographer_id)

@router.get("/user/{user_id}", response_model=PhotographerInDB)
def read_photographer_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_photographer = crud_photographer.get_photographer_by_user_id(db, user_id)
    if db_photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return db_photographer