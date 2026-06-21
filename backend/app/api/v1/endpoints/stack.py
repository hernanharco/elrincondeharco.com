from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.core.cloudinary import upload_image
from app.models.stack import Stack
from app.schemas.stack import StackCreate, StackUpdate, StackResponse
from app.core.security import get_current_admin_user
from typing import Any, Dict

async def get_stack_form(
    name: str = Form(...),
    category: str = Form(...),
    icon: str = Form(...),
    description: str = Form(...),
    color: str = Form(...),
    border: str = Form(...),
    glow: str = Form(...),
) -> StackCreate:
    return StackCreate(
        name=name,
        category=category,
        icon=icon,
        description=description,
        color=color,
        border=border,
        glow=glow
    )

async def get_stack_update_form(
    name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    border: Optional[str] = Form(None),
    glow: Optional[str] = Form(None),
) -> StackUpdate:
    return StackUpdate(
        name=name,
        category=category,
        icon=icon,
        description=description,
        color=color,
        border=border,
        glow=glow
    )

router = APIRouter()

@router.get("/", response_model=list[StackResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Stack))
    return result.scalars().all()

@router.get("/{id}", response_model=StackResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Stack, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Stack no encontrado")
    return obj

@router.post("/", response_model=StackResponse)
async def create(
    form_data: StackCreate = Depends(get_stack_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    db_obj = Stack(**form_data.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.put("/{id}", response_model=StackResponse)
async def update(
    id: int,
    form_data: StackUpdate = Depends(get_stack_update_form),
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Stack, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Stack no encontrado")
    for key, value in form_data.model_dump(exclude_none=True).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.delete("/{id}")
async def delete(id: int, db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Stack, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Stack no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Stack eliminado"}
