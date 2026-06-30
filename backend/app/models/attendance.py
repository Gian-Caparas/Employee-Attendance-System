import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base


class AttendanceStatus(str, enum.Enum):
    present = "present"
    late = "late"
    absent = "absent"
    on_leave = "on_leave"
    half_day = "half_day"
    holiday = "holiday"


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time_in = Column(Time, nullable=True)
    time_out = Column(Time, nullable=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.present, nullable=False, index=True)
    minutes_late = Column(Integer, default=0)
    source = Column(String(20), default="manual")  # manual | ocr_import | api
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = relationship("Employee", back_populates="attendance_records")
