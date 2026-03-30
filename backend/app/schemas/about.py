from pydantic import BaseModel
from typing import Optional

class AboutCreate(BaseModel):
    title: str
    description: str
    location: str
    years_experience: str
    team_name: str
    leadership_title: str
    leadership_desc: str
    experience_title: str
    experience_desc: str

class AboutUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    years_experience: Optional[str] = None
    team_name: Optional[str] = None
    leadership_title: Optional[str] = None
    leadership_desc: Optional[str] = None
    experience_title: Optional[str] = None
    experience_desc: Optional[str] = None

class AboutResponse(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str] = None
    location: str
    years_experience: str
    team_name: str
    leadership_title: str
    leadership_desc: str
    experience_title: str
    experience_desc: str

    class Config:
        model_config = {"from_attributes": True}
