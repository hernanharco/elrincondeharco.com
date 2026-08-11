"""add cta fields to site_settings

Revision ID: 6a7b8c9d0e1f
Revises: 5e6f7a8b9c0d
Create Date: 2026-07-29 14:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision: str = "6a7b8c9d0e1f"
down_revision: Union[str, None] = "5e6f7a8b9c0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("site_settings", sa.Column("cta_title", sa.Text(), nullable=True))
    op.add_column(
        "site_settings", sa.Column("cta_description", sa.Text(), nullable=True)
    )
    op.add_column("site_settings", sa.Column("cta_features", JSONB(), nullable=True))
    op.add_column(
        "site_settings", sa.Column("cta_primary_text", sa.String(100), nullable=True)
    )
    op.add_column(
        "site_settings", sa.Column("cta_secondary_text", sa.String(100), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("site_settings", "cta_secondary_text")
    op.drop_column("site_settings", "cta_primary_text")
    op.drop_column("site_settings", "cta_features")
    op.drop_column("site_settings", "cta_description")
    op.drop_column("site_settings", "cta_title")
