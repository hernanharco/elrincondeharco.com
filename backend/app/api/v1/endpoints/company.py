"""
company.py — Proxy a authCore para datos de empresa de la landing page.
La landing page (Portfolio) muestra datos de contacto que viven en authCore.
"""

import os
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, status
import httpx
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()

# Qué usuario de authCore es el dueño de esta landing page
# Se configura via env var COMPANY_USER_ID en el docker-compose
COMPANY_USER_ID = os.getenv("COMPANY_USER_ID", "1")


class CompanyPublic(BaseModel):
    company_name: str
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    contact_name: Optional[str] = None


@router.get("/public", response_model=CompanyPublic)
async def get_landing_company():
    """
    Obtiene los datos públicos de la empresa dueña de esta landing page.
    Hace proxy a authCore (endpoint público /api/v1/companies/{user_id}/public).
    """
    # authCore puede estar en localhost:8000 (desarrollo) o authcore-api:8000 (Docker)
    authcore_base = settings.authcore_jwks_url.removesuffix("/.well-known/jwks.json")
    url = f"{authcore_base}/api/v1/company/{COMPANY_USER_ID}/public"

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil de empresa no configurado. Contactá al administrador.",
                )
            if response.status_code != 200:
                logging.error(f"Error fetching company from authCore: {response.status_code}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Error al obtener datos de la empresa",
                )
            return response.json()

        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo contactar con el servidor de autenticación",
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="El servidor de autenticación tardó demasiado en responder",
            )
