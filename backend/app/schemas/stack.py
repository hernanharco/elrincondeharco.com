from pydantic import BaseModel
from typing import Optional

class StackCreate(BaseModel):
    name: str
    category: str
    icon: str
    description: str
    color: str
    border: str
    glow: str

class StackUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    border: Optional[str] = None
    glow: Optional[str] = None

class StackResponse(BaseModel):
    id: int
    name: str
    category: str
    icon: str
    description: str
    color: str
    border: str
    glow: str

    class Config:
        model_config = {"from_attributes": True}
