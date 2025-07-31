from sqlalchemy.orm import Session
from collections import defaultdict
from models.schedule import WorkingHoursTemplate, BlockedSlot
from schemas.schedule import WorkingHoursCreate, BlockedSlotCreate
from models.order import Order, OrderStatusEnum
from datetime import datetime, timedelta

def add_working_hours(db: Session, photographer_id: int, entry: WorkingHoursCreate):
    obj = WorkingHoursTemplate(**entry.dict(), photographer_id=photographer_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_working_hours(db: Session, photographer_id: int):
    return db.query(WorkingHoursTemplate).filter_by(photographer_id=photographer_id).all()

def add_blocked_slot(db: Session, photographer_id: int, entry: BlockedSlotCreate):
    obj = BlockedSlot(**entry.dict(), photographer_id=photographer_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_blocked(db: Session, photographer_id: int, start, end):
    return db.query(BlockedSlot).filter(
        BlockedSlot.photographer_id == photographer_id,
        BlockedSlot.date >= start,
        BlockedSlot.date <= end
    ).all()

def get_booked_slots(db: Session, photographer_id: int, start, end):
    orders = db.query(Order).filter(
        Order.photographer_id == photographer_id,
        Order.shoot_date >= start,
        Order.shoot_date <= end,
        Order.status != OrderStatusEnum.cancelled,
        Order.status != OrderStatusEnum.completed
    ).all()

    booked = defaultdict(list)
    for order in orders:
        start_dt = datetime.combine(order.shoot_date, order.start_time)
        for i in range(order.duration):
            slot_time = (start_dt + timedelta(hours=i)).time()
            booked[order.shoot_date].append(slot_time)

    return booked