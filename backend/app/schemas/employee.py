from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    employee_code: str
    full_name: str
    email: EmailStr
    department: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    date_hired: Optional[datetime] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[int] = None


class EmployeeOut(EmployeeBase):
    id: int
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True
