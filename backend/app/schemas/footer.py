from pydantic import BaseModel
from typing import Optional, List, Dict

class FooterCreate(BaseModel):
    name: str
    description: str
    location: str
    email: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    quick_links: List[Dict[str, str]]

class FooterUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    quick_links: Optional[List[Dict[str, str]]] = None

class FooterResponse(BaseModel):
    id: int
    name: str
    description: str
    location: str
    email: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    quick_links: List[Dict[str, str]]

    class Config:
        orm_mode = True
