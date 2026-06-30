from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(120), nullable=False, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    department = Column(String(100), index=True)
    position = Column(String(100))
    phone = Column(String(30))
    date_hired = Column(DateTime)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attendance_records = relationship(
        "AttendanceRecord", back_populates="employee", cascade="all, delete-orphan"
    )
