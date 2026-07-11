from pydantic import BaseModel
from typing import Optional


class TestimonialCreate(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    content: str
    rating: int = 5
    avatar_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class TestimonialResponse(BaseModel):
    id: int
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    content: str
    rating: int
    avatar_url: Optional[str] = None
    is_active: bool
    sort_order: int

    model_config = {"from_attributes": True}
