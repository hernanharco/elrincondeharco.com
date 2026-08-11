"""
Radar Endpoint — Contrato que Radar consume para buscar servicios/productos.

Este endpoint es parte del contrato TENANT → RADAR.
Cada cliente que activa Radar debe implementar este mismo endpoint
en su backend para que el asistente pueda consultar datos del negocio.

Radar llama:
  GET /api/v1/radar/search?q=desarrollo+web
  Header: X-API-Key: <clave_compartida>

Además expone /api/v1/radar/token: un endpoint SSO para el modo embebido.
El CRM (ya autenticado) pide un token del Radar y se lo pasa al iframe
por postMessage, evitando un segundo login.
"""

import httpx
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, cast, String
from typing import Any, Dict, Optional

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
from app.core.security import get_current_admin_user

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


@router.get("/token")
async def radar_token(
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    """
    SSO para el modo embebido: devuelve un token del Radar para que el
    iframe cargue sin pedir login. Protegido por la auth del CRM
    (cookie authCore válida).
    """
    api_url = settings.radar_api_url
    api_password = settings.radar_api_password
    if not api_url or not api_password:
        raise HTTPException(
            status_code=503,
            detail="Radar SSO not configured (RADAR_API_URL / RADAR_API_PASSWORD)",
        )

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{api_url}/api/auth/login",
                json={"password": api_password},
            )
        if resp.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Radar login failed: HTTP {resp.status_code}",
            )
        data = resp.json()
        token = data.get("token")
        if not token:
            raise HTTPException(status_code=502, detail="Radar login returned no token")
        return {"token": token}
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Radar unreachable: {exc}") from exc
