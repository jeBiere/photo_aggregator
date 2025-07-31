from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from models.user import User, UserRole
from schemas.order import OrderCreate, OrderUpdate, OrderInDB
from crud import order as crud_order
from crud import studio as crud_studio
from db import get_db
from utils.jwt_utils import require_photographer, get_current_user
from utils.email_utils import schedule_studio_notification
from authx import TokenPayload  # если используешь

router = APIRouter()

@router.post("/", response_model=OrderInDB)
def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    db_order = crud_order.create_order(db, order)

    if order.studio_id:
        studio = crud_studio.get_studio(db, order.studio_id)
        if studio and studio.email:
            schedule_studio_notification(
                background_tasks,
                studio_email=studio.email,
                order_info=order.dict()
            )

    return db_order
@router.get("/", response_model=List[OrderInDB])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.get_orders(db, skip=skip, limit=limit)

@router.get("/me", response_model=List[OrderInDB])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == UserRole.client or current_user.role == UserRole.admin:
        return crud_order.get_orders_by_user_id(db, user_id=current_user.user_id)

    elif current_user.role == UserRole.photographer:
        orders = crud_order.get_orders_by_photographer_user_id(db, user_id=current_user.user_id)
        if orders is None:
            raise HTTPException(status_code=404, detail="Photographer profile not found")
        return orders

    else:
        raise HTTPException(status_code=403, detail=f"Unsupported role {current_user.role} !")


@router.get("/{order_id}", response_model=OrderInDB)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.put("/{order_id}", response_model=OrderInDB)
def update_order(order_id: int, updates: OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud_order.update_order(db, order_id, updates)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", response_model=OrderInDB)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.delete_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/{order_id}/cancel", response_model=OrderInDB)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.cancel_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/{order_id}/confirm", response_model=OrderInDB)
def confirm_order(
    order_id: int,
    db: Session = Depends(get_db),
    payload: TokenPayload = Depends(require_photographer)
):
    db_order = crud_order.confirm_order_by_photographer(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found or not in pending state")
    return db_order

@router.post("/{order_id}/complete", response_model=OrderInDB)
def complete_order(
    order_id: int,
    db: Session = Depends(get_db),
    payload: TokenPayload = Depends(require_photographer)
):
    db_order = crud_order.complete_order_by_photographer(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found or not in pending state")
    return db_order

