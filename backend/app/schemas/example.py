from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ExampleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ExampleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ExampleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
