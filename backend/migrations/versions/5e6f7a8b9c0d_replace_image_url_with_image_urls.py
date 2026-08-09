"""replace image_url with image_urls (JSONB) in projects

Revision ID: 5e6f7a8b9c0d
Revises: 4d5e6f7a8b9c
Create Date: 2026-07-29 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "5e6f7a8b9c0d"
down_revision: Union[str, None] = "4d5e6f7a8b9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Agregar columna image_urls como JSONB nullable
    op.add_column("projects", sa.Column("image_urls", JSONB(), nullable=True))

    # 2. Migrar datos existentes de image_url a image_urls
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "UPDATE projects SET image_urls = "
            "CASE WHEN image_url IS NOT NULL AND image_url != '' "
            "THEN jsonb_build_array(image_url) "
            "ELSE '[]'::jsonb END"
        )
    )

    # 3. Hacer image_urls NOT NULL
    op.alter_column("projects", "image_urls", nullable=False)

    # 4. Eliminar columna vieja
    op.drop_column("projects", "image_url")


def downgrade() -> None:
    # 1. Restaurar image_url
    op.add_column("projects", sa.Column("image_url", sa.VARCHAR(), nullable=True))

    # 2. Volcar primera imagen de vuelta
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "UPDATE projects SET image_url = "
            "CASE "
            "WHEN jsonb_array_length(image_urls) > 0 "
            "THEN image_urls->>0 "
            "ELSE NULL END"
        )
    )

    # 3. Eliminar image_urls
    op.drop_column("projects", "image_urls")
