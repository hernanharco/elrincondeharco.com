from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.core.cloudinary import upload_image
from app.models.about import About
from app.schemas.about import AboutCreate, AboutUpdate, AboutResponse

async def get_about_form(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    years_experience: str = Form(...),
    team_name: str = Form(...),
    leadership_title: str = Form(...),
    leadership_desc: str = Form(...),
    experience_title: str = Form(...),
    experience_desc: str = Form(...),
) -> AboutCreate:
    return AboutCreate(
        title=title,
        description=description,
        location=location,
        years_experience=years_experience,
        team_name=team_name,
        leadership_title=leadership_title,
        leadership_desc=leadership_desc,
        experience_title=experience_title,
        experience_desc=experience_desc
    )

async def get_about_update_form(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    years_experience: Optional[str] = Form(None),
    team_name: Optional[str] = Form(None),
    leadership_title: Optional[str] = Form(None),
    leadership_desc: Optional[str] = Form(None),
    experience_title: Optional[str] = Form(None),
    experience_desc: Optional[str] = Form(None),
) -> AboutUpdate:
    return AboutUpdate(
        title=title,
        description=description,
        location=location,
        years_experience=years_experience,
        team_name=team_name,
        leadership_title=leadership_title,
        leadership_desc=leadership_desc,
        experience_title=experience_title,
        experience_desc=experience_desc
    )

router = APIRouter()

@router.get("/", response_model=list[AboutResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(About))
    return result.scalars().all()

@router.get("/{id}", response_model=AboutResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(About, id)
    if not obj:
        raise HTTPException(status_code=404, detail="About no encontrado")
    return obj

@router.get("/latest/", response_model=AboutResponse)
async def get_latest(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(About).order_by(About.id.desc()).limit(1)
    )
    obj = result.scalars().first()
    if not obj:
        raise HTTPException(status_code=404, detail="No hay registros")
    return obj

@router.post("/", response_model=AboutResponse)
async def create(
    form_data: AboutCreate = Depends(get_about_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    image_url = None
    if image and image.filename:
        image_url = await upload_image(image)
    db_obj = About(**form_data.dict(), image_url=image_url)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=AboutResponse)
async def update(
    id: int,
    form_data: AboutUpdate = Depends(get_about_update_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    obj = await db.get(About, id)
    if not obj:
        raise HTTPException(status_code=404, detail="About no encontrado")
    for key, value in form_data.dict(exclude_none=True).items():
        setattr(obj, key, value)
    if image and image.filename:
        obj.image_url = await upload_image(image)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(About, id)
    if not obj:
        raise HTTPException(status_code=404, detail="About no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "About eliminado"}
