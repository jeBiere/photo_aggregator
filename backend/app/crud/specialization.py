from sqlalchemy.orm import Session
from models.specialization import PhotographerSpecialization
from schemas.specialization import PhotographerSpecializationCreate

def get_specialization(db: Session, photographer_id: int, specialization: str):
    return db.query(PhotographerSpecialization).filter(
        PhotographerSpecialization.photographer_id == photographer_id,
        PhotographerSpecialization.specialization == specialization
    ).first()

def get_specializations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PhotographerSpecialization).offset(skip).limit(limit).all()

def create_specialization(db: Session, specialization: PhotographerSpecializationCreate):
    db_specialization = PhotographerSpecialization(**specialization.dict())
    db.add(db_specialization)
    db.commit()
    db.refresh(db_specialization)
    return db_specialization

def delete_specialization(db: Session, photographer_id: int, specialization: str):
    db_specialization = db.query(PhotographerSpecialization).filter(
        PhotographerSpecialization.photographer_id == photographer_id,
        PhotographerSpecialization.specialization == specialization
    ).first()
    if db_specialization:
        db.delete(db_specialization)
        db.commit()
    return db_specialization
