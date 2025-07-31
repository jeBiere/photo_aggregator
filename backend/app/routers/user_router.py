import os
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from schemas.user import UserCreate, UserUpdate, UserInDB, UserLogin
from crud.user import (create_user, get_user, get_users, update_user, delete_user, get_user_by_email, get_user_by_id, get_user_orders, get_user_reviews, update_avatar_url)
from models.user import User

from schemas.order import OrderInDB
from models.order import Order

from schemas.reviews import ReviewInDB
from models.reviews import Review

from db import get_db

from utils.jwt_utils import ( verify_password, get_token, get_current_user, security, require_admin, SECRET_KEY)

from authx import TokenPayload

AVATAR_FOLDER = "static/avatars"

router = APIRouter()

@router.get("/", response_model=List[UserInDB])
async def read_users(
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
    admin: dict = Depends(require_admin)
):
    return get_users(db)

@router.post("/avatar", summary="Загрузить аватарку текущего пользователя")
async def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Можно загружать только изображения.")

    os.makedirs(AVATAR_FOLDER, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    filename = f"user_{current_user.user_id}_{uuid4().hex}{ext}"
    filepath = os.path.join(AVATAR_FOLDER, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    public_path = f"/static/avatars/{filename}"
    updated_user = update_avatar_url(db, current_user.user_id, public_path)

    return {"avatar_url": updated_user.avatar_url}


@router.get("/me", response_model=UserInDB)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)  # Заменяем логику с декодированием токена
):
    return current_user  # Прямо возвращаем текущего пользователя

@router.get("/reviews", response_model=List[ReviewInDB])
def read_user_reviews(
    user_id: int,
    db: Session = Depends(get_db)
):
    if not db.query(User).filter(User.user_id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    
    return get_user_reviews(db, user_id=user_id)

@router.get("/user_by_login/{user_login}", response_model=UserInDB)
async def read_user(
    user_login: str, 
    db: Session = Depends(get_db)
):
    user = get_user(db, user_login)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/user_by_id/{user_id}", response_model=UserInDB)
async def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", response_model=UserInDB, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.login):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db, user)

@router.post("/login")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = get_user(db, user_login.login)
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid login or password")
    
    access_token = security.create_access_token(
        uid=str(user.user_id), 
        data={"role": user.role}
    )
    return {"access_token": access_token}

@router.put("/{user_login}", response_model=UserInDB)
async def modify_user(
    user_login: str, 
    user: UserUpdate, 
    db: Session = Depends(get_db)
):
    updated_user = update_user(db, user_login, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_login}", response_model=dict)
async def remove_user(
    user_login: str, 
    db: Session = Depends(get_db)
):
    if not delete_user(db, user_login):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


