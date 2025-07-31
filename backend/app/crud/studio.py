from sqlalchemy.orm import Session
from models.studio import PhotoStudio
from schemas.studio import PhotoStudioCreate, PhotoStudioUpdate

def get_studio(db: Session, studio_id: int):
    return db.query(PhotoStudio).filter(PhotoStudio.studio_id == studio_id).first()

def get_studios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PhotoStudio).filter(PhotoStudio.is_active == True).offset(skip).limit(limit).all()


def create_studio(db: Session, studio: PhotoStudioCreate):
    studio_data = studio.dict()
    
    if studio_data.get("website_url"):
        studio_data["website_url"] = str(studio_data["website_url"])
    if studio_data.get("profile_picture_url"):
        studio_data["profile_picture_url"] = str(studio_data["profile_picture_url"])

    db_studio = PhotoStudio(**studio_data)
    db.add(db_studio)
    db.commit()
    db.refresh(db_studio)
    return db_studio

def update_studio(db: Session, studio_id: int, studio: PhotoStudioUpdate):
    db_studio = db.query(PhotoStudio).filter(PhotoStudio.studio_id == studio_id).first()
    if db_studio:
        for key, value in studio.dict(exclude_unset=True).items():
            setattr(db_studio, key, value)
        db.commit()
        db.refresh(db_studio)
        return db_studio
    return None

def delete_studio(db: Session, studio_id: int):
    db_studio = db.query(PhotoStudio).filter(PhotoStudio.studio_id == studio_id).first()
    if db_studio:
        db.delete(db_studio)
        db.commit()
    return db_studio
