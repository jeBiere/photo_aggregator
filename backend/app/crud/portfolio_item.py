from sqlalchemy.orm import Session
from models.portfolio_item import PortfolioItem
from models.photographer import Photographer
from schemas.portfolio_item import PortfolioItemCreate, PortfolioItemUpdate
from datetime import datetime
import os
import shutil

STATIC_PORTFOLIO_PATH = "static/portfolio"

def get_portfolio_item(db: Session, item_id: int):
    return db.query(PortfolioItem).filter(PortfolioItem.item_id == item_id).first()

def get_portfolio_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PortfolioItem).offset(skip).limit(limit).all()

def create_portfolio_item(db: Session, item: PortfolioItemCreate, photographer_id: int):
    db_item = PortfolioItem(**item.dict(), photographer_id=photographer_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_portfolio_item(db: Session, item_id: int, updates: PortfolioItemUpdate):
    db_item = db.query(PortfolioItem).filter(PortfolioItem.item_id == item_id).first()
    if db_item:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
        db_item.created_at = datetime.utcnow()
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_portfolio_item(db: Session, item_id: int):
    db_item = db.query(PortfolioItem).filter(PortfolioItem.item_id == item_id).first()
    if db_item:
        folder_path = os.path.join(STATIC_PORTFOLIO_PATH, str(item_id))
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        db.delete(db_item)
        db.commit()
    return db_item

def get_my_portfolio_items(db: Session, user_id: int):
    photographer = db.query(Photographer).filter(Photographer.user_id == user_id).first()
    if not photographer:
        return []

    return db.query(PortfolioItem).filter(PortfolioItem.photographer_id == photographer.photographer_id).all()

def get_portfolio_items_by_photographer_id(db: Session, photographer_id: int):
    return db.query(PortfolioItem).filter(PortfolioItem.photographer_id == photographer_id).all()
