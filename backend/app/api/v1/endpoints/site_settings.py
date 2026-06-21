from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import json
from app.db.session import get_db
from app.models.site_settings import SiteSettings
from app.schemas.site_settings import (
    SiteSettingsCreate,
    SiteSettingsUpdate,
    SiteSettingsResponse,
)
from app.core.security import get_current_admin_user
from typing import Any, Dict

# --- Helpers de Limpieza ---

def clean_none_values(data: dict) -> dict:
    """Convierte strings 'None', 'null' o vacíos en None reales de Python."""
    if not data:
        return {}
    clean_data = {}
    for k, v in data.items():
        if v is None or str(v).lower() in ["none", "null", "undefined", ""]:
            clean_data[k] = None
        else:
            clean_data[k] = v
    return clean_data

async def get_site_settings_form(
    brand_name: str = Form(...),
    site_url: str = Form(...),
    legal_name: str = Form(...),
    slogan: Optional[str] = Form(None),
    copyright_notice: str = Form(...),
    contact_email: str = Form(...),
    social_networks: Optional[str] = Form(None),
    is_active: bool = Form(True),
) -> SiteSettingsCreate:
    # Procesar JSON de redes sociales
    try:
        sn_dict = json.loads(social_networks) if social_networks else {}
        sn_dict = clean_none_values(sn_dict)
    except (json.JSONDecodeError, TypeError):
        sn_dict = {}

    return SiteSettingsCreate(
        brand_name=brand_name,
        site_url=site_url,
        legal_name=legal_name,
        slogan=None if str(slogan).lower() == "none" else slogan,
        copyright_notice=copyright_notice,
        contact_email=contact_email,
        social_networks=sn_dict,
        is_active=is_active,
    )

async def get_site_settings_update_form(
    brand_name: Optional[str] = Form(None),
    site_url: Optional[str] = Form(None),
    legal_name: Optional[str] = Form(None),
    slogan: Optional[str] = Form(None),
    copyright_notice: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    social_networks: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
) -> SiteSettingsUpdate:
    # Procesar JSON de redes sociales para actualización
    sn_dict = None
    if social_networks:
        try:
            sn_dict = json.loads(social_networks)
            sn_dict = clean_none_values(sn_dict)
        except (json.JSONDecodeError, TypeError):
            sn_dict = None

    return SiteSettingsUpdate(
        brand_name=brand_name,
        site_url=site_url,
        legal_name=legal_name,
        slogan=None if str(slogan).lower() == "none" else slogan,
        copyright_notice=copyright_notice,
        contact_email=contact_email,
        social_networks=sn_dict,
        is_active=is_active,
    )

# --- Router y Endpoints ---

router = APIRouter()

# 1. RUTA CRÍTICA: /latest/ va primero para evitar que coincida con /{id}
@router.get("/latest/", response_model=SiteSettingsResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SiteSettings)
        .where(SiteSettings.is_active == True)
        .order_by(SiteSettings.id.desc())
        .limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="No hay configuraciones activas")
    return obj

@router.get("/", response_model=List[SiteSettingsResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SiteSettings))
    return result.scalars().all()

# 2. RUTA DINÁMICA: /{id} va después de las estáticas
@router.get("/{id}", response_model=SiteSettingsResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(SiteSettings, id)
    if not obj:
        raise HTTPException(status_code=404, detail="SiteSettings no encontrado")
    return obj

@router.post("/", response_model=SiteSettingsResponse)
async def create(
    form_data: SiteSettingsCreate = Depends(get_site_settings_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    # En Pydantic v2 se prefiere model_dump() sobre dict()
    db_obj = SiteSettings(**form_data.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=SiteSettingsResponse)
async def update(
    id: int,
    form_data: SiteSettingsUpdate = Depends(get_site_settings_update_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(SiteSettings, id)
    if not obj:
        raise HTTPException(status_code=404, detail="SiteSettings no encontrado")

    # Al usar mode='json', Pydantic convierte automáticamente:
    # 1. HttpUrl -> str (Esto arregla el error de psycopg/SQLAlchemy)
    # 2. Submodelos -> dict (Esto evita el AttributeError)
    update_data = form_data.model_dump(exclude_none=True, mode='json')

    for key, value in update_data.items():
        setattr(obj, key, value)

    try:
        await db.commit()
        await db.refresh(obj)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")
        
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(SiteSettings, id)
    if not obj:
        raise HTTPException(status_code=404, detail="SiteSettings no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "SiteSettings eliminado"}