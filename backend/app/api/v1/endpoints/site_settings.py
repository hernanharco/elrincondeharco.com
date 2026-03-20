from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import json
from app.db.session import get_db
from app.models.site_settings import SiteSettings
from app.schemas.site_settings import SiteSettingsCreate, SiteSettingsUpdate, SiteSettingsResponse


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
    social_networks_dict = json.loads(social_networks) if social_networks else {}
    
    return SiteSettingsCreate(
        brand_name=brand_name,
        site_url=site_url,
        legal_name=legal_name,
        slogan=slogan,
        copyright_notice=copyright_notice,
        contact_email=contact_email,
        social_networks=social_networks_dict,
        is_active=is_active
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
    social_networks_dict = json.loads(social_networks) if social_networks else None
    
    return SiteSettingsUpdate(
        brand_name=brand_name,
        site_url=site_url,
        legal_name=legal_name,
        slogan=slogan,
        copyright_notice=copyright_notice,
        contact_email=contact_email,
        social_networks=social_networks_dict,
        is_active=is_active
    )


router = APIRouter()


@router.get("/", response_model=list[SiteSettingsResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SiteSettings))
    return result.scalars().all()


@router.get("/{id}", response_model=SiteSettingsResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(SiteSettings, id)
    if not obj:
        raise HTTPException(status_code=404, detail="SiteSettings no encontrado")
    return obj


@router.get("/latest/", response_model=SiteSettingsResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SiteSettings).where(SiteSettings.is_active == True).order_by(SiteSettings.id.desc()).limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="No hay configuraciones activas")
    return obj


@router.post("/", response_model=SiteSettingsResponse)
async def create(
    form_data: SiteSettingsCreate = Depends(get_site_settings_form),
    db: AsyncSession = Depends(get_db)
):
    db_obj = SiteSettings(**form_data.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.put("/{id}", response_model=SiteSettingsResponse)
async def update(
    id: int,
    form_data: SiteSettingsUpdate = Depends(get_site_settings_update_form),
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(SiteSettings, id)
    if not obj:
        raise HTTPException(status_code=404, detail="SiteSettings no encontrado")
    
    for key, value in form_data.dict(exclude_none=True).items():
        setattr(obj, key, value)
    
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(SiteSettings, id)
    if not obj:
        raise HTTPException(status_code=404, detail="SiteSettings no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "SiteSettings eliminado"}
