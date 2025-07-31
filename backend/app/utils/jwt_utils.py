
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload
from fastapi import APIRouter, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer
from models.user import User
from db import get_db

SECRET_KEY = "2f75b31bde99b877f24f0bdba7365ce2a807252a580337accb789e95a0988009f0c0460b2a0b3f5906619b3c38a5bcc9d9f0529b9ef5a88d1d8e533cd9998e8c9072f438ed22ee3123d29545521db565a724d8d1c251b48d2344f118fcd1edf75a7271e89cf08a5d46281a566f0410499d97c679c8a9391de3989643471b343b07e46450ae26997b840aa1192729fe9a69fc1384b1cc9de71b8f5fd452cba6946f77355b214f49b3713d7184ee0b0f53b2c99d37f5f5994d6c1192ae901657965b6127841f3076945c0a8c7a9429d837c944229b9c9f4f639a8cbe87f6a67aedab9b5fa5e42fe5ca65b1cab1bf721fffe1faae51f325a57defce00a21ce0738b"
config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = SECRET_KEY
config.JWT_TOKEN_LOCATION = ["headers"]
config.JWT_HEADER_NAME = "Authorization"
config.JWT_HEADER_TYPE = "Bearer"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = AuthX(config=config)

sec = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_token(authorization: str = Security(sec)):
    return authorization.credentials

async def get_current_user(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
) -> User:
    try:
        payload = TokenPayload.decode(token, key=config.JWT_SECRET_KEY)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.sub
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user_id missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

async def require_admin(token: str = Depends(get_token)):
    payload = TokenPayload.decode(token, key=config.JWT_SECRET_KEY)
    
    if not payload.role == "admin":
        raise HTTPException(status_code=403, detail="User is not an admin")
    
    return payload

async def require_photographer(token: str = Depends(get_token)):
    payload = TokenPayload.decode(token, key=config.JWT_SECRET_KEY)
    
    if payload.role == "admin" or payload.role == 'photographer':
        return payload
    raise HTTPException(status_code=403, detail="User is not a photographer")