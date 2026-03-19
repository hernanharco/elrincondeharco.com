from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.models.example import Example
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_examples(db: AsyncSession = Depends(get_db)):
    """Get all examples from the database."""
    result = await db.execute("SELECT * FROM examples")
    examples = result.fetchall()
    return [
        {"id": row[0], "name": row[1], "description": row[2], "created_at": row[3]}
        for row in examples
    ]


@router.post("/", response_model=dict)
async def create_example(
    name: str,
    description: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Create a new example."""
    from sqlalchemy import text
    query = text(
        "INSERT INTO examples (name, description) VALUES (:name, :description) RETURNING id, name, description, created_at"
    )
    result = await db.execute(query, {"name": name, "description": description})
    await db.commit()
    row = result.fetchone()
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "created_at": row[3]
    }


@router.get("/health")
async def example_health():
    """Health check for example endpoint."""
    return {"status": "healthy", "endpoint": "example"}
