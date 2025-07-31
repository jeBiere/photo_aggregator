from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.portfolio_item import PortfolioItemCreate, PortfolioItemUpdate, PortfolioItemInDB
from models.user import User, UserRole
from models.photographer import Photographer
from crud import portfolio_item as crud_portfolio_item
from db import get_db
from utils.jwt_utils import require_photographer, get_current_user

router = APIRouter()

@router.post("/", response_model=PortfolioItemInDB)
def create_portfolio_item(
    item: PortfolioItemCreate,
    db: Session = Depends(get_db),
    user_payload = Depends(require_photographer) 
):
    user_id = int(user_payload.sub)

    photographer = db.query(Photographer).filter(Photographer.user_id == user_id).first()
    if not photographer:
        raise HTTPException(status_code=403, detail="Photographer record not found")

    return crud_portfolio_item.create_portfolio_item(
        db=db,
        item=item,
        photographer_id=photographer.photographer_id
    )

@router.get("/", response_model=List[PortfolioItemInDB])
def read_portfolio_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_portfolio_item.get_portfolio_items(db, skip=skip, limit=limit)

@router.get("/me", response_model=List[PortfolioItemInDB])
def read_my_portfolio_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.photographer:
        raise HTTPException(status_code=403, detail=f"Only photographers can view their portfolio, but your is {current_user.role}")

    return crud_portfolio_item.get_my_portfolio_items(db, current_user.user_id)

@router.get("/item_by_id/{item_id}", response_model=PortfolioItemInDB)
def read_portfolio_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_portfolio_item.get_portfolio_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Portfolio Item not found")
    return db_item


@router.get("/item_by_photographer/{photographer_id}", response_model=List[PortfolioItemInDB])
def read_portfolio_by_photographer_id(
    photographer_id: int,
    db: Session = Depends(get_db)
):
    return crud_portfolio_item.get_portfolio_items_by_photographer_id(db, photographer_id)

@router.put("/{item_id}", response_model=PortfolioItemInDB)
def update_portfolio_item(item_id: int, updates: PortfolioItemUpdate, db: Session = Depends(get_db)):
    db_item = crud_portfolio_item.update_portfolio_item(db, item_id, updates)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Portfolio Item not found")
    return db_item

@router.delete("/{item_id}", response_model=PortfolioItemInDB)
def delete_portfolio_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud_portfolio_item.delete_portfolio_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Portfolio Item not found")
    return db_item
