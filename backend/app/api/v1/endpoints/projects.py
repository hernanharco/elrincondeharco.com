from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import json
from app.db.session import get_db
from app.core.cloudinary import upload_image
from app.models.projects import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectResponse
from app.core.security import get_current_admin_user
from typing import Any, Dict

async def get_project_form(
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form(...),  # JSON string
    icon_name: str = Form(...),
    color: str = Form(...),
    demo_url: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
) -> ProjectCreate:
    return ProjectCreate(
        title=title,
        description=description,
        tags=json.loads(tags),
        icon_name=icon_name,
        color=color,
        demo_url=demo_url,
        github_url=github_url
    )

async def get_project_update_form(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    icon_name: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    demo_url: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
) -> ProjectUpdate:
    return ProjectUpdate(
        title=title,
        description=description,
        tags=json.loads(tags) if tags else None,
        icon_name=icon_name,
        color=color,
        demo_url=demo_url,
        github_url=github_url
    )

router = APIRouter()

@router.get("/", response_model=list[ProjectResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    return result.scalars().all()

@router.get("/{id}", response_model=ProjectResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Project, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project no encontrado")
    return obj

@router.post("/", response_model=ProjectResponse)
async def create(
    form_data: ProjectCreate = Depends(get_project_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    image_url = None
    if image and image.filename:
        image_url = await upload_image(image)
    db_obj = Project(**form_data.dict(), image_url=image_url)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=ProjectResponse)
async def update(
    id: int,
    form_data: ProjectUpdate = Depends(get_project_update_form),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Project, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project no encontrado")
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
    obj = await db.get(Project, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Project eliminado"}
