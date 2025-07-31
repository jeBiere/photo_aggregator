from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from sqlalchemy.orm import Session
from typing import List
from schemas.schedule import WorkingHoursCreate, BlockedSlotCreate
from models.photographer import Photographer
from models.schedule import WorkingHoursTemplate
from crud import schedule as crud
from utils.jwt_utils import require_photographer, get_token, SECRET_KEY
from utils.date_availability_generator import generate_availability
from db import get_db
from authx import TokenPayload

router = APIRouter()

@router.post("/working-hours")
def create_working_hours(data: WorkingHoursCreate, token: str = Depends(get_token), db: Session = Depends(get_db)):
    payload = TokenPayload.decode(token, key = SECRET_KEY)
    if payload.role != "photographer":
        raise HTTPException(status_code=403, detail="Only photographers can edit schedule.")
    photographer = db.query(Photographer).filter_by(user_id=int(payload.sub)).first()
    return crud.add_working_hours(db, photographer_id=photographer.photographer_id, entry=data)

@router.get("/working-hours/me")
def get_my_working_hours(
    payload: TokenPayload = Depends(require_photographer),
    db: Session = Depends(get_db)
):
    photographer = db.query(Photographer).filter_by(user_id=int(payload.sub)).first()
    if not photographer:
        raise HTTPException(status_code=404, detail="Photographer profile not found.")
    hours = db.query(WorkingHoursTemplate).filter_by(photographer_id=photographer.photographer_id).all()
    return hours


@router.post("/blocked-slots")
def create_blocked_slot(data: BlockedSlotCreate, token: str = Depends(get_token), db: Session = Depends(get_db)):
    payload = TokenPayload.decode(token, key = SECRET_KEY)
    photographer = db.query(Photographer).filter_by(user_id=int(payload.sub)).first()
    return crud.add_blocked_slot(db, photographer_id=photographer.photographer_id, entry=data)

@router.get("/availability/{photographer_id}")
def get_availability(photographer_id: int, start: date = Query(...), end: date = Query(...), db: Session = Depends(get_db)):
    if start > end:
        raise HTTPException(status_code=400, detail="Invalid date range")
    working_hours = crud.get_working_hours(db, photographer_id)
    blocked = crud.get_blocked(db, photographer_id, start, end)
    booked = crud.get_booked_slots(db, photographer_id, start, end)
    return generate_availability(working_hours, blocked, booked, start, end)