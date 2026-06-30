from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str = "employee"


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True
