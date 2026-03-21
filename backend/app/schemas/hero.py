from pydantic import BaseModel
from typing import Optional

class HeroCreate(BaseModel):
    title: str
    subtitle: str
    description: str
    background_image: Optional[str] = None
    contact_button_text: str
    cv_button_text: str
    image_url: Optional[str] = None
    cv_url: Optional[str] = None

class HeroUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    background_image: Optional[str] = None
    contact_button_text: Optional[str] = None
    cv_button_text: Optional[str] = None
    image_url: Optional[str] = None
    cv_url: Optional[str] = None

class HeroResponse(BaseModel):
    id: int
    title: str
    subtitle: str
    description: str
    background_image: Optional[str] = None
    contact_button_text: str
    cv_button_text: str
    image_url: Optional[str] = None
    cv_url: Optional[str] = None

    class Config:
        from_attributes = True
