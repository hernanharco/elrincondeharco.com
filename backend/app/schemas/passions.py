from pydantic import BaseModel
from typing import Optional

class PassionCreate(BaseModel):
    title: str
    description: str
    family_title: str
    family_desc: str
    games_title: str
    games_desc: str
    coding_title: str
    coding_desc: str

class PassionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    family_title: Optional[str] = None
    family_desc: Optional[str] = None
    games_title: Optional[str] = None
    games_desc: Optional[str] = None
    coding_title: Optional[str] = None
    coding_desc: Optional[str] = None

class PassionResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str] = None
    family_title: str
    family_desc: str
    games_title: str
    games_desc: str
    coding_title: str
    coding_desc: str

    model_config = {"from_attributes": True}
