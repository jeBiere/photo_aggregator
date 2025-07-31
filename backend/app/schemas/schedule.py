from pydantic import BaseModel
from datetime import date, time
from typing import Optional

# Базовая схема для расписания
class WorkingHoursCreate(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time

class BlockedSlotCreate(BaseModel):
    date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    reason: Optional[str] = None