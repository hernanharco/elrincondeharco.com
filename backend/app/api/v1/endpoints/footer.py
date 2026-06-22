from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import json
from app.db.session import get_db

from app.models.footer import Footer
from app.schemas.footer import FooterCreate, FooterUpdate, FooterResponse
from app.core.security import get_current_admin_user
from typing import Any, Dict

async def get_footer_form(
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    email: str = Form(...),
    github_url: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    twitter_url: Optional[str] = Form(None),
    quick_links: str = Form(...),  # JSON string
) -> FooterCreate:
    return FooterCreate(
        name=name,
        description=description,
        location=location,
        email=email,
        github_url=github_url,
        linkedin_url=linkedin_url,
        twitter_url=twitter_url,
        quick_links=json.loads(quick_links)
    )

async def get_footer_update_form(
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    twitter_url: Optional[str] = Form(None),
    quick_links: Optional[str] = Form(None),
) -> FooterUpdate:
    return FooterUpdate(
        name=name,
        description=description,
        location=location,
        email=email,
        github_url=github_url,
        linkedin_url=linkedin_url,
        twitter_url=twitter_url,
        quick_links=json.loads(quick_links) if quick_links else None
    )

router = APIRouter()

@router.get("/", response_model=list[FooterResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Footer))
    return result.scalars().all()

@router.get("/latest/", response_model=FooterResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Footer).order_by(Footer.id.desc()).limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="No hay registros")
    return obj

@router.get("/{id}", response_model=FooterResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Footer, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Footer no encontrado")
    return obj

@router.post("/", response_model=FooterResponse)
async def create(
    form_data: FooterCreate = Depends(get_footer_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    db_obj = Footer(**form_data.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=FooterResponse)
async def update(
    id: int,
    form_data: FooterUpdate = Depends(get_footer_update_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Footer, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Footer no encontrado")
    for key, value in form_data.model_dump(exclude_none=True).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Footer, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Footer no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Footer eliminado"}
