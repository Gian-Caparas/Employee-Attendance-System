import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    hr = "hr"
    manager = "manager"
    employee = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
