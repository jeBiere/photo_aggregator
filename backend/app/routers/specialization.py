from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.specialization import PhotographerSpecializationCreate, PhotographerSpecializationInDB
from crud import specialization as crud_specialization
from db import get_db

router = APIRouter()

@router.post("/", response_model=PhotographerSpecializationInDB)
def create_specialization(specialization: PhotographerSpecializationCreate, db: Session = Depends(get_db)):
    return crud_specialization.create_specialization(db, specialization)

@router.get("/", response_model=List[PhotographerSpecializationInDB])
def read_specializations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_specialization.get_specializations(db, skip=skip, limit=limit)

@router.get("/{photographer_id}/{specialization}", response_model=PhotographerSpecializationInDB)
def read_specialization(photographer_id: int, specialization: str, db: Session = Depends(get_db)):
    db_specialization = crud_specialization.get_specialization(db, photographer_id, specialization)
    if db_specialization is None:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return db_specialization

@router.delete("/{photographer_id}/{specialization}", response_model=PhotographerSpecializationInDB)
def delete_specialization(photographer_id: int, specialization: str, db: Session = Depends(get_db)):
    db_specialization = crud_specialization.delete_specialization(db, photographer_id, specialization)
    if db_specialization is None:
        raise HTTPException(status_code=404, detail="Specialization not found")
    return db_specialization
