from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import json
from app.db.session import get_db
from app.core.cloudinary import process_file_upload
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
    image_urls: Optional[str] = Form("[]"),  # JSON array de URLs existentes
) -> ProjectCreate:
    try:
        parsed_tags = json.loads(tags)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="tags debe ser un JSON válido")
    try:
        parsed_image_urls = json.loads(image_urls)
    except json.JSONDecodeError:
        parsed_image_urls = []
    return ProjectCreate(
        title=title,
        description=description,
        image_urls=parsed_image_urls,
        tags=parsed_tags,
        icon_name=icon_name,
        color=color,
        demo_url=demo_url,
        github_url=github_url,
    )


async def get_project_update_form(
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    icon_name: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    demo_url: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
    image_urls: Optional[str] = Form(None),  # JSON array de URLs existentes
) -> ProjectUpdate:
    parsed_tags = None
    if tags:
        try:
            parsed_tags = json.loads(tags)
        except json.JSONDecodeError:
            raise HTTPException(status_code=422, detail="tags debe ser un JSON válido")
    parsed_image_urls = None
    if image_urls:
        try:
            parsed_image_urls = json.loads(image_urls)
        except json.JSONDecodeError:
            parsed_image_urls = None
    return ProjectUpdate(
        title=title,
        description=description,
        image_urls=parsed_image_urls,
        tags=parsed_tags,
        icon_name=icon_name,
        color=color,
        demo_url=demo_url,
        github_url=github_url,
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
    images: Optional[List[UploadFile]] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    # Procesar imágenes subidas
    new_urls = []
    if images:
        for img in images:
            if img.filename and img.filename != "":
                url = await process_file_upload(img)
                if url:
                    new_urls.append(url)

    all_urls = form_data.image_urls + new_urls
    db_obj = Project(
        **form_data.model_dump(exclude={"image_urls"}), image_urls=all_urls
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.put("/{id}", response_model=ProjectResponse)
async def update(
    id: int,
    form_data: ProjectUpdate = Depends(get_project_update_form),
    images: Optional[List[UploadFile]] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Project, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project no encontrado")

    # Procesar imágenes nuevas
    new_urls = []
    if images:
        for img in images:
            if img.filename and img.filename != "":
                url = await process_file_upload(img)
                if url:
                    new_urls.append(url)

    # Merge: si viene image_urls, reemplazar; si no, mantener existentes + nuevas
    existing = list(obj.image_urls) if obj.image_urls else []
    if form_data.image_urls is not None:
        existing = form_data.image_urls
    obj.image_urls = existing + new_urls

    # Actualizar resto de campos
    for key in (
        "title",
        "description",
        "tags",
        "icon_name",
        "color",
        "demo_url",
        "github_url",
    ):
        value = getattr(form_data, key, None)
        if value is not None:
            setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}")
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Project, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Project eliminado"}
