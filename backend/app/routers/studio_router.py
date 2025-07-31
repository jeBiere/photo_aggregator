from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.studio import PhotoStudioCreate, PhotoStudioUpdate, PhotoStudioInDB
from crud import studio as crud_studio
from db import get_db
from utils.jwt_utils import require_admin

router = APIRouter()

@router.post("/", response_model=PhotoStudioInDB)
def create_studio(studio: PhotoStudioCreate, db: Session = Depends(get_db), token = Depends(require_admin)):
    return crud_studio.create_studio(db, studio)

@router.get("/", response_model=List[PhotoStudioInDB])
def read_studios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_studio.get_studios(db, skip=skip, limit=limit)

@router.get("/{studio_id}", response_model=PhotoStudioInDB)
def read_studio(studio_id: int, db: Session = Depends(get_db)):
    db_studio = crud_studio.get_studio(db, studio_id)
    if db_studio is None:
        raise HTTPException(status_code=404, detail="Studio not found")
    return db_studio

@router.put("/{studio_id}", response_model=PhotoStudioInDB)
def update_studio(studio_id: int, studio: PhotoStudioUpdate, db: Session = Depends(get_db), token = Depends(require_admin)):
    db_studio = crud_studio.update_studio(db, studio_id, studio)
    if db_studio is None:
        raise HTTPException(status_code=404, detail="Studio not found")
    return db_studio

@router.delete("/{studio_id}", response_model=PhotoStudioInDB)
def delete_studio(studio_id: int, db: Session = Depends(get_db), token = Depends(require_admin)):
    db_studio = crud_studio.delete_studio(db, studio_id)
    if db_studio is None:
        raise HTTPException(status_code=404, detail="Studio not found")
    return db_studio
