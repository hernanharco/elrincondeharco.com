from pydantic import BaseModel
from typing import Optional, List


class SectorCreate(BaseModel):
    name: str
    client_name: str
    description: Optional[str] = None
    icon_path: str
    color_gradient: str
    sort_order: int = 0
    project_ids: List[int] = []


class SectorUpdate(BaseModel):
    name: Optional[str] = None
    client_name: Optional[str] = None
    description: Optional[str] = None
    icon_path: Optional[str] = None
    color_gradient: Optional[str] = None
    sort_order: Optional[int] = None
    project_ids: Optional[List[int]] = None


class SectorResponse(BaseModel):
    id: int
    name: str
    client_name: str
    description: Optional[str] = None
    icon_path: str
    color_gradient: str
    sort_order: int
    project_ids: List[int]

    model_config = {"from_attributes": True}
