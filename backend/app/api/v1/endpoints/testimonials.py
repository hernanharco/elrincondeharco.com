from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any, Dict

from app.db.session import get_db
from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate, TestimonialResponse
from app.core.security import get_current_admin_user


router = APIRouter()


@router.get("/", response_model=list[TestimonialResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Testimonial)
        .filter(Testimonial.is_active == True)
        .order_by(Testimonial.sort_order)
    )
    return result.scalars().all()


@router.get("/all", response_model=list[TestimonialResponse])
async def get_all_admin(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Testimonial).order_by(Testimonial.sort_order)
    )
    return result.scalars().all()


@router.get("/{id}", response_model=TestimonialResponse)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Testimonial, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    return obj


@router.post("/", response_model=TestimonialResponse)
async def create(
    form_data: TestimonialCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    db_obj = Testimonial(**form_data.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.put("/{id}", response_model=TestimonialResponse)
async def update(
    id: int,
    form_data: TestimonialUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_admin_user),
):
    obj = await db.get(Testimonial, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    for key, value in form_data.model_dump(exclude_none=True).items():
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
    obj = await db.get(Testimonial, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Testimonio no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Testimonio eliminado"}
