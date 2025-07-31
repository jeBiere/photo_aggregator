from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from crud import portfolio_photo as crud_photo
from db import get_db
from schemas.portfolio_photo import PortfolioPhotoInDB
from utils.jwt_utils import require_photographer  # если ограничиваем только фотографам

STATIC_PORTFOLIO_PATH = "static/portfolio"

router = APIRouter()


@router.post("/{item_id}/photos", response_model=List[PortfolioPhotoInDB])
def upload_photos(
    item_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_photographer),
):
    saved_photos = []
    item_folder = os.path.join(STATIC_PORTFOLIO_PATH, str(item_id))
    os.makedirs(item_folder, exist_ok=True)

    for file in files:
        file_path = os.path.join(item_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        db_photo = crud_photo.create_portfolio_photo(db, item_id=item_id, file_path=file_path)
        saved_photos.append(db_photo)

    return saved_photos


@router.get("/{item_id}/photos", response_model=List[PortfolioPhotoInDB])
def get_photos(item_id: int, db: Session = Depends(get_db)):
    return crud_photo.get_photos_by_item(db, item_id)


@router.delete("/photos/{photo_id}", response_model=PortfolioPhotoInDB)
def delete_photo(photo_id: int, db: Session = Depends(get_db), user=Depends(require_photographer)):
    photo = crud_photo.delete_photo(db, photo_id)
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")

    if os.path.exists(photo.file_path):
        os.remove(photo.file_path)

    return photo
