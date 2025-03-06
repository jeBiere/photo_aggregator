from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer
from typing import List
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate, UserInDB, UserLogin
from models.user import User  # Импорт модели User
from crud.user import get_users, get_user, create_user, update_user, delete_user
from db import get_db
from authx import AuthX, AuthXConfig, TokenPayload
from utils.jwt_utils import verify_password

config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = "2f75b31bde99b877f24f0bdba7365ce2a807252a580337accb789e95a0988009f0c0460b2a0b3f5906619b3c38a5bcc9d9f0529b9ef5a88d1d8e533cd9998e8c9072f438ed22ee3123d29545521db565a724d8d1c251b48d2344f118fcd1edf75a7271e89cf08a5d46281a566f0410499d97c679c8a9391de3989643471b343b07e46450ae26997b840aa1192729fe9a69fc1384b1cc9de71b8f5fd452cba6946f77355b214f49b3713d7184ee0b0f53b2c99d37f5f5994d6c1192ae901657965b6127841f3076945c0a8c7a9429d837c944229b9c9f4f639a8cbe87f6a67aedab9b5fa5e42fe5ca65b1cab1bf721fffe1faae51f325a57defce00a21ce0738b"
config.JWT_TOKEN_LOCATION = ["headers"]
config.JWT_HEADER_NAME = "Authorization"
config.JWT_HEADER_TYPE = "Bearer"

security = AuthX(config=config)

sec = HTTPBearer()

router = APIRouter()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_token(authorization: str = Security(sec)):
    return authorization.credentials

@router.get("/", response_model=List[UserInDB])
async def read_users(db: Session = Depends(get_db), token: str = Depends(get_token)):
    return get_users(db)

@router.get("/{user_login}", response_model=UserInDB)
async def read_user(user_login: str, db: Session = Depends(get_db)):
    user = get_user(db, user_login)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=201)
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login", status_code=200)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.login == user_login.login).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login or password")
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid login or password")
    
    access_token = security.create_access_token(uid=user.login)   
    
    return {"access_token": access_token}

@router.put("/{user_login}", response_model=UserInDB)
async def modify_user(user_login: str, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_login, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_login}", response_model=dict)
async def remove_user(user_login: str, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_login)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}



