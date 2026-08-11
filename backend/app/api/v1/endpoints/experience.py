from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Any, Dict
from app.db.session import get_db
from app.models.experience import ExperienceSection
from app.schemas.experience import (
    ExperienceSectionCreate,
    ExperienceSectionUpdate,
    ExperienceSectionResponse,
)
from app.core.security import get_current_admin_user

router = APIRouter()


async def get_experience_form(
    tagline: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
) -> ExperienceSectionCreate:
    return ExperienceSectionCreate(
        tagline=tagline,
        title=title,
        description=description,
    )


async def get_experience_update_form(
    tagline: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
) -> ExperienceSectionUpdate:
    return ExperienceSectionUpdate(
        tagline=tagline,
        title=title,
        description=description,
    )


@router.get("/latest/", response_model=ExperienceSectionResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ExperienceSection).order_by(ExperienceSection.id.desc()).limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(
            status_code=404, detail="No hay configuración de experiencia"
        )
    return obj


@router.post("/", response_model=ExperienceSectionResponse)
async def create(
    form_data: ExperienceSectionCreate = Depends(get_experience_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    db_obj = ExperienceSection(**form_data.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.put("/{id}", response_model=ExperienceSectionResponse)
async def update(
    id: int,
    form_data: ExperienceSectionUpdate = Depends(get_experience_update_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(ExperienceSection, id)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Configuración de experiencia no encontrada"
        )

    for key, value in form_data.model_dump(exclude_none=True).items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj
