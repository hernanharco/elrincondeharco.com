from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
