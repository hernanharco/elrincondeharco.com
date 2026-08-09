"""
Radar Search Schemas — formato de intercambio entre Radar y los tenants.
Es el CONTRATO que cualquier tenant debe implementar para que Radar
pueda consultar sus productos/servicios.
"""

from pydantic import BaseModel
from typing import Optional


class RadarSearchItem(BaseModel):
    """Un item del resultado de búsqueda."""

    id: str
    name: str
    description: str
    price: Optional[str] = None
    currency: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[dict] = None


class RadarSearchResponse(BaseModel):
    """Respuesta estándar que Radar espera."""

    items: list[RadarSearchItem]


class RadarOverviewItem(BaseModel):
    """Un item resumido del overview del tenant."""

    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[dict] = None


class RadarOverviewResponse(BaseModel):
    """Resumen de la información del tenant: proyectos, stacks, sectores, showroom."""

    projects: list[RadarOverviewItem]
    stacks: list[RadarOverviewItem]
    sectors: list[RadarOverviewItem]
    showroom: list[RadarOverviewItem]
