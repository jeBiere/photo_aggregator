from typing import List, Optional
from sqlalchemy.orm import Session
from models.user import User
from models.order import Order
from models.reviews import Review
from schemas.user import UserCreate, UserUpdate, UserInDB
from schemas.order import OrderInDB
from schemas.reviews import ReviewInDB
from datetime import datetime
from utils.jwt_utils import pwd_context

def create_user(db: Session, user: UserCreate) -> UserInDB:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        email=user.email,
        phone=user.phone,
        city=user.city,
        password_hash=hashed_password,
        avatar_url=user.avatar_url,
        status=user.status,
        role=user.role,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserInDB.from_orm(db_user)

def get_user(db: Session, user_login: str) -> Optional[UserInDB]:
    db_user = db.query(User).filter(User.login == user_login).first()
    return UserInDB.from_orm(db_user) if db_user else None

def get_user_by_email(db: Session, email: str) -> Optional[UserInDB]:
    db_user = db.query(User).filter(User.email == email).first()
    return UserInDB.from_orm(db_user) if db_user else None

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserInDB]:
    db_users = db.query(User).offset(skip).limit(limit).all()
    return [UserInDB.from_orm(user) for user in db_users]

def update_user(db: Session, user_login: str, user_update: UserUpdate) -> Optional[UserInDB]:
    db_user = db.query(User).filter(User.login == user_login).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    if 'password' in update_data:
        update_data['password_hash'] = pwd_context.hash(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return UserInDB.from_orm(db_user)

def delete_user(db: Session, user_login: str) -> bool:

    db_user = db.query(User).filter(User.login == user_login).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def get_user_by_id(db: Session, user_id: int) -> Optional[UserInDB]:
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[OrderInDB]:
    db_orders = db.query(Order)\
        .filter(Order.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return [OrderInDB.from_orm(order) for order in db_orders]

def get_user_reviews(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[ReviewInDB]:
    db_reviews = db.query(Review)\
        .filter(Review.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return [ReviewInDB.from_orm(review) for review in db_reviews]

def update_avatar_url(db: Session, user_id: int, avatar_url: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    user.avatar_url = avatar_url
    db.commit()
    db.refresh(user)
    return user
