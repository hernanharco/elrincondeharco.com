from pydantic import BaseModel
from typing import Optional


class ExperienceSectionCreate(BaseModel):
    tagline: str
    title: str
    description: str


class ExperienceSectionUpdate(BaseModel):
    tagline: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class ExperienceSectionResponse(BaseModel):
    id: int
    tagline: str
    title: str
    description: str

    model_config = {"from_attributes": True}
