from pydantic import BaseModel
from typing import Optional, List


class ProjectCreate(BaseModel):
    title: str
    description: str
    image_urls: List[str] = []
    tags: List[str]
    icon_name: str
    color: str
    demo_url: Optional[str] = None
    github_url: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    icon_name: Optional[str] = None
    color: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    image_urls: List[str] = []
    tags: List[str]
    icon_name: str
    color: str
    demo_url: Optional[str] = None
    github_url: Optional[str] = None

    model_config = {"from_attributes": True}
