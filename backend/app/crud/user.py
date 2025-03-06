from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserInDB
from typing import List
from datetime import datetime, timedelta
import utils.jwt_utils as jwt_utils
from sqlalchemy.orm import Session

# Инициализация контекста для хеширования паролей
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, login: str) -> UserInDB:
    user = db.query(User).filter(User.login == login).first()
    if user:
        return UserInDB.from_orm(user)
    raise HTTPException(status_code=404, detail="User not found")

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[UserInDB]:
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserInDB.from_orm(user) for user in users]

def create_user(db: Session, user_data: UserCreate) -> UserInDB:
    # Хешируем пароль перед добавлением в базу данных
    hashed_password = jwt_utils.pwd_context.hash(user_data.password)
    db_user = User(
        login=user_data.login,
        email=user_data.email,
        hashed_password=hashed_password,
        registration_date=user_data.registration_date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserInDB.from_orm(db_user)

def update_user(db: Session, login: str, user_data: UserUpdate) -> UserInDB:
    db_user = db.query(User).filter(User.login == login).first()
    if db_user:
        update_data = user_data.dict(exclude_unset=True)
        # Если пароль изменён, хешируем новый
        if "password" in update_data:
            update_data["hashed_password"] = jwt_utils.pwd_context.hash(update_data["password"])
            del update_data["password"]  # Убираем старое поле password
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return UserInDB.from_orm(db_user)
    raise HTTPException(status_code=404, detail="User not found")

def delete_user(db: Session, login: str):
    db_user = db.query(User).filter(User.login == login).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


