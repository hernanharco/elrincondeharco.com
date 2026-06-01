from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.core.cloudinary import upload_image
from app.models.passions import Passion
from app.schemas.passions import PassionCreate, PassionUpdate, PassionResponse
from app.core.security import get_current_admin_user
from typing import Any, Dict

async def get_passion_form(
    title: str = Form(...),
    description: str = Form(...),
    family_title: str = Form(...),
    family_desc: str = Form(...),
    games_title: str = Form(...),
    games_desc: str = Form(...),
    coding_title: str = Form(...),
    coding_desc: str = Form(...),
) -> PassionCreate:
    return PassionCreate(
        title=title,
        description=description,
        family_title=family_title,
        family_desc=family_desc,
        games_title=games_title,
        games_desc=games_desc,
        coding_title=coding_title,
        coding_desc=coding_desc
    )

async def get_passion_update_form(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    family_title: Optional[str] = Form(None),
    family_desc: Optional[str] = Form(None),
    games_title: Optional[str] = Form(None),
    games_desc: Optional[str] = Form(None),
    coding_title: Optional[str] = Form(None),
    coding_desc: Optional[str] = Form(None),
) -> PassionUpdate:
    return PassionUpdate(
        title=title,
        description=description,
        family_title=family_title,
        family_desc=family_desc,
        games_title=games_title,
        games_desc=games_desc,
        coding_title=coding_title,
        coding_desc=coding_desc
    )

router = APIRouter()

@router.get("/", response_model=list[PassionResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Passion))
    return result.scalars().all()

@router.get("/{id}", response_model=PassionResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Passion, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Passion no encontrado")
    return obj

@router.get("/latest/", response_model=PassionResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Passion).order_by(Passion.id.desc()).limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="No hay registros")
    return obj

@router.post("/", response_model=PassionResponse)
async def create(
    form_data: PassionCreate = Depends(get_passion_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    image_url = None
    if image and image.filename:
        image_url = await upload_image(image)
    db_obj = Passion(**form_data.dict(), image_url=image_url)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=PassionResponse)
async def update(
    id: int,
    form_data: PassionUpdate = Depends(get_passion_update_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Passion, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Passion no encontrado")
    for key, value in form_data.dict(exclude_none=True).items():
        setattr(obj, key, value)
    if image and image.filename:
        obj.image_url = await upload_image(image)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get
    obj = await db.get(Passion, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Passion no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Passion eliminado"}
