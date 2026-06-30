from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel


class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    status: str = "present"
    minutes_late: int = 0
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(BaseModel):
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    status: Optional[str] = None
    minutes_late: Optional[int] = None
    notes: Optional[str] = None


class AttendanceOut(AttendanceBase):
    id: int
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
