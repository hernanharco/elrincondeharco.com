from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate, ExampleResponse

router = APIRouter()


@router.get("/", response_model=List[ExampleResponse])
async def get_examples(db: AsyncSession = Depends(get_db)):
    """Get all examples from the database."""
    result = await db.execute(select(Example).order_by(Example.id))
    return result.scalars().all()


@router.post("/", response_model=ExampleResponse, status_code=201)
async def create_example(data: ExampleCreate, db: AsyncSession = Depends(get_db)):
    """Create a new example."""
    db_obj = Example(**data.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.get("/{id}", response_model=ExampleResponse)
async def get_example(id: int, db: AsyncSession = Depends(get_db)):
    """Get a single example by ID."""
    obj = await db.get(Example, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Example no encontrado")
    return obj


@router.put("/{id}", response_model=ExampleResponse)
async def update_example(
    id: int, data: ExampleUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an existing example."""
    obj = await db.get(Example, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Example no encontrado")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(obj, key, value)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}")
async def delete_example(id: int, db: AsyncSession = Depends(get_db)):
    """Delete an example."""
    obj = await db.get(Example, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Example no encontrado")
    await db.delete(obj)
    await db.commit()
    return {"detail": "Example eliminado"}


@router.get("/health")
async def example_health():
    """Health check for example endpoint."""
    return {"status": "healthy", "endpoint": "example"}
