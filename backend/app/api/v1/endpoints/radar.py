"""
Radar Endpoint — Contrato que Radar consume para buscar servicios/productos.

Este endpoint es parte del contrato TENANT → RADAR.
Cada cliente que activa Radar debe implementar este mismo endpoint
en su backend para que el asistente pueda consultar datos del negocio.

Radar llama:
  GET /api/v1/radar/search?q=desarrollo+web
  Header: X-API-Key: <clave_compartida>
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, cast, String
from typing import Optional

from app.db.session import get_db
from app.models.projects import Project
from app.models.stack import Stack
from app.models.sector import Sector
from app.models.showroom import Showroom
from app.schemas.radar import (
    RadarSearchResponse,
    RadarSearchItem,
    RadarOverviewResponse,
    RadarOverviewItem,
)
from app.core.config import settings

router = APIRouter()


async def verify_radar_key(x_api_key: Optional[str] = Header(None)):
    """Valida que la llamada venga de Radar (o de quien tenga la API key)."""
    expected_key = settings.radar_api_key
    if not expected_key:
        # Si no hay clave configurada, el endpoint está deshabilitado
        raise HTTPException(status_code=503, detail="Radar integration not configured")
    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.get("/search", response_model=RadarSearchResponse)
async def search(
    q: str,
    db: AsyncSession = Depends(get_db),
    _=Depends(verify_radar_key),
):
    """
    Busca servicios/proyectos de Harco que coincidan con el query.

    Radar llama a este endpoint cuando el asistente necesita responder
    una pregunta sobre los servicios que ofrece Harco.
    """
    if not q or not q.strip():
        return RadarSearchResponse(items=[])

    query = q.strip()

    # Buscar en projects: title, description, tags
    stmt = select(Project).where(
        or_(
            Project.title.ilike(f"%{query}%"),
            Project.description.ilike(f"%{query}%"),
            cast(Project.tags, String).ilike(f"%{query}%"),
        )
    )
    result = await db.execute(stmt)
    projects = result.scalars().all()

    items = []
    for project in projects:
        # image_urls es JSONB array, tomar la primera o null
        first_image = (
            project.image_urls[0]
            if project.image_urls and len(project.image_urls) > 0
            else None
        )
        items.append(
            RadarSearchItem(
                id=str(project.id),
                name=project.title,
                description=project.description,
                image=first_image,
                url=project.demo_url,
                metadata={
                    "tags": project.tags,
                    "icon_name": project.icon_name,
                    "color": project.color,
                    "github_url": project.github_url,
                },
            )
        )

    return RadarSearchResponse(items=items)


@router.get("/overview", response_model=RadarOverviewResponse)
async def overview(
    db: AsyncSession = Depends(get_db),
    _=Depends(verify_radar_key),
):
    """
    Devuelve un resumen de toda la información del tenant (proyectos,
    stacks, sectores y showroom) para que el asistente del dueño pueda
    responder preguntas generales sobre el negocio.
    """
    project_result = await db.execute(select(Project).order_by(Project.id))
    projects = [
        RadarOverviewItem(
            name=p.title,
            description=p.description,
            url=p.demo_url,
            metadata={
                "tags": p.tags,
                "icon_name": p.icon_name,
                "color": p.color,
            },
        )
        for p in project_result.scalars().all()
    ]

    stack_result = await db.execute(select(Stack).order_by(Stack.id))
    stacks = [
        RadarOverviewItem(
            name=s.name,
            description=s.description,
            metadata={"category": s.category, "icon": s.icon},
        )
        for s in stack_result.scalars().all()
    ]

    sector_result = await db.execute(select(Sector).order_by(Sector.id))
    sectors = [
        RadarOverviewItem(
            name=s.name,
            description=s.description,
            metadata={"client_name": s.client_name},
        )
        for s in sector_result.scalars().all()
    ]

    showroom_result = await db.execute(select(Showroom).order_by(Showroom.id))
    showroom = [
        RadarOverviewItem(
            name=sh.title,
            description=sh.description,
            url=sh.deploy_url,
            metadata={"category": sh.category},
        )
        for sh in showroom_result.scalars().all()
    ]

    return RadarOverviewResponse(
        projects=projects,
        stacks=stacks,
        sectors=sectors,
        showroom=showroom,
    )
