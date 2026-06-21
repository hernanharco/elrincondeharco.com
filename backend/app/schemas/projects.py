from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.dialects.postgresql import JSONB

class ProjectCreate(BaseModel):
    title: str
    description: str
    tags: List[str]
    icon_name: str
    color: str
    demo_url: Optional[str] = None
    github_url: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    icon_name: Optional[str] = None
    color: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str] = None
    tags: List[str]
    icon_name: str
    color: str
    demo_url: Optional[str] = None
    github_url: Optional[str] = None

    model_config = {"from_attributes": True}
