from sqlalchemy.orm import Session
from models.photographer import Photographer
from models.order import Order, OrderStatusEnum
from schemas.order import OrderCreate, OrderUpdate
from datetime import datetime, timedelta

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.order_id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def get_orders_by_user_id(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_orders_by_photographer_user_id(db: Session, user_id: int):
    photographer = db.query(Photographer).filter(Photographer.user_id == user_id).first()
    
    if not photographer:
        return None 

    return db.query(Order).filter(Order.photographer_id == photographer.photographer_id).all()

def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, updates: OrderUpdate):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_order, field, value)
        db_order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

def cancel_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order:
        db_order.status = OrderStatusEnum.cancelled
        db_order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
    return db_order

def confirm_order_by_photographer(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order and db_order.status == OrderStatusEnum.pending:
        db_order.status = OrderStatusEnum.in_progress
        db_order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

def complete_order_by_photographer(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order and db_order.status != OrderStatusEnum.cancelled:
        db_order.status = OrderStatusEnum.completed
        db_order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

def delete_old_cancelled_orders(db: Session):
    cutoff_date = datetime.utcnow() - timedelta(weeks=26)  # 6 месяцев

    deleted_orders = db.query(Order).filter(
        Order.status == "cancelled",
        Order.updated_at < cutoff_date
    ).delete(synchronize_session=False)

    db.commit() 
    print(f"Deleted {deleted_orders} old cancelled orders.")