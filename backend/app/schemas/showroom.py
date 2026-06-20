from pydantic import BaseModel
from typing import Optional

class ShowroomCreate(BaseModel):
    title: str
    description: str
    category: str
    deploy_url: Optional[str] = None

class ShowroomUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    deploy_url: Optional[str] = None

class ShowroomResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    deploy_url: Optional[str] = None
    image_url: Optional[str] = None

    model_config = {"from_attributes": True}
