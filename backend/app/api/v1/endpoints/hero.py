from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.core.cloudinary import process_file_upload
from app.models.hero import Hero
from app.schemas.hero import HeroCreate, HeroUpdate, HeroResponse
from app.core.security import get_current_admin_user
from typing import Any, Dict

async def get_hero_form(
    title: str = Form(...),
    subtitle: str = Form(...),
    description: str = Form(...),
    background_image: Optional[str] = Form(None),
    contact_button_text: str = Form(...),
    cv_button_text: str = Form(...),
) -> HeroCreate:
    return HeroCreate(
        title=title,
        subtitle=subtitle,
        description=description,
        background_image=background_image,
        contact_button_text=contact_button_text,
        cv_button_text=cv_button_text
    )

async def get_hero_update_form(
    title: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    background_image: Optional[str] = Form(None),
    contact_button_text: Optional[str] = Form(None),
    cv_button_text: Optional[str] = Form(None),
) -> HeroUpdate:
    return HeroUpdate(
        title=title,
        subtitle=subtitle,
        description=description,
        background_image=background_image,
        contact_button_text=contact_button_text,
        cv_button_text=cv_button_text
    )

router = APIRouter()

@router.get("/", response_model=list[HeroResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hero))
    return result.scalars().all()

@router.get("/latest/", response_model=HeroResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Hero).order_by(Hero.id.desc()).limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="No hay registros")
    return obj

@router.get("/{id}", response_model=HeroResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Hero, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hero no encontrado")
    return obj

@router.post("/", response_model=HeroResponse)
async def create(
    form_data: HeroCreate = Depends(get_hero_form),
    image: Optional[UploadFile] = File(None),
    cv_file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    image_url = await process_file_upload(image)
    cv_url = await process_file_upload(cv_file)

    db_obj = Hero(**form_data.model_dump(), image_url=image_url, cv_url=cv_url)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=HeroResponse)
async def update(
    id: int,
    form_data: HeroUpdate = Depends(get_hero_update_form),
    image: Optional[UploadFile] = File(None),
    cv_file: Optional[UploadFile] = File(None), # <-- Nuevo parámetro
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Hero, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hero no encontrado")
    
    for key, value in form_data.model_dump(exclude_none=True).items():
        setattr(obj, key, value)
    
    # Manejo de archivos (imagen y CV)
    image_url = await process_file_upload(image)
    if image_url:
        obj.image_url = image_url

    cv_url = await process_file_upload(cv_file)
    if cv_url:
        obj.cv_url = cv_url
        
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Hero, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hero no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Hero eliminado"}
