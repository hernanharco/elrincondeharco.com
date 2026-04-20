from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.core.cloudinary import upload_image
from app.models.showroom import Showroom
from app.schemas.showroom import ShowroomCreate, ShowroomUpdate, ShowroomResponse

async def get_showroom_form(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    deploy_url: Optional[str] = Form(None),
) -> ShowroomCreate:
    return ShowroomCreate(
        title=title,
        description=description,
        category=category,
        deploy_url=deploy_url
    )

async def get_showroom_update_form(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    deploy_url: Optional[str] = Form(None),
) -> ShowroomUpdate:
    return ShowroomUpdate(
        title=title,
        description=description,
        category=category,
        deploy_url=deploy_url
    )

router = APIRouter()

@router.get("/", response_model=list[ShowroomResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Showroom))
    return result.scalars().all()

@router.get("/{id}", response_model=ShowroomResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Showroom, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Showroom no encontrado")
    return obj

@router.post("/", response_model=ShowroomResponse)
async def create(
    form_data: ShowroomCreate = Depends(get_showroom_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    image_url = None
    if image and image.filename:
        image_url = await upload_image(image)
    db_obj = Showroom(**form_data.dict(), image_url=image_url)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=ShowroomResponse)
async def update(
    id: int,
    form_data: ShowroomUpdate = Depends(get_showroom_update_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(Showroom, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Showroom no encontrado")
    for key, value in form_data.dict(exclude_none=True).items():
        setattr(obj, key, value)
    if image and image.filename:
        obj.image_url = await upload_image(image)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Showroom, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Showroom no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Showroom eliminado"}
