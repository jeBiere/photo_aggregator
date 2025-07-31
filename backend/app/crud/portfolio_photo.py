from sqlalchemy.orm import Session
from models.portfolio_photo import PortfolioPhoto
from schemas.portfolio_photo import PortfolioPhotoInDB
from typing import List, Optional

def create_portfolio_photo(db: Session, item_id: int, file_path: str) -> PortfolioPhoto:
    photo = PortfolioPhoto(item_id=item_id, file_path=file_path)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

def get_photos_by_item(db: Session, item_id: int) -> List[PortfolioPhoto]:
    return db.query(PortfolioPhoto).filter(PortfolioPhoto.item_id == item_id).all()

def delete_photo(db: Session, photo_id: int) -> Optional[PortfolioPhoto]:
    photo = db.query(PortfolioPhoto).filter(PortfolioPhoto.photo_id == photo_id).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo
