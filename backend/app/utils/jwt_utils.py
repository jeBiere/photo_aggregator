import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Security, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

ECRET_KEY = "2f75b31bde99b877f24f0bdba7365ce2a807252a580337accb789e95a0988009f0c0460b2a0b3f5906619b3c38a5bcc9d9f0529b9ef5a88d1d8e533cd9998e8c9072f438ed22ee3123d29545521db565a724d8d1c251b48d2344f118fcd1edf75a7271e89cf08a5d46281a566f0410499d97c679c8a9391de3989643471b343b07e46450ae26997b840aa1192729fe9a69fc1384b1cc9de71b8f5fd452cba6946f77355b214f49b3713d7184ee0b0f53b2c99d37f5f5994d6c1192ae901657965b6127841f3076945c0a8c7a9429d837c944229b9c9f4f639a8cbe87f6a67aedab9b5fa5e42fe5ca65b1cab1bf721fffe1faae51f325a57defce00a21ce0738b"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
    
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return user_id
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")
