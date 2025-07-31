from sqlalchemy.orm import Session
from typing import List, Optional
from models.studio import PhotoStudio

def create_studio_photo(db: Session, studio_id: int, file_path: str) -> PhotoStudio:
    photo = PhotoStudio(studio_id=studio_id, file_path=file_path)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

def get_photos_by_studio(db: Session, studio_id: int) -> List[PhotoStudio]:
    return db.query(PhotoStudio).filter(PhotoStudio.studio_id == studio_id).all()

def delete_photo(db: Session, photo_id: int) -> Optional[PhotoStudio]:
    photo = db.query(PhotoStudio).filter(PhotoStudio.photo_id == photo_id).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo
