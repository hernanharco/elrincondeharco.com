"""add sectors and testimonials tables

Revision ID: 2a3b4c5d6e7f
Revises: 7969bead0e27
Create Date: 2026-07-11

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '2a3b4c5d6e7f'
down_revision: Union[str, None] = '7969bead0e27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # sectors table
    op.create_table(
        'sectors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('client_name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon_path', sa.String(), nullable=False),
        sa.Column('color_gradient', sa.String(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('project_ids', JSONB(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_sectors_id'), 'sectors', ['id'], unique=False)

    # testimonials table
    op.create_table(
        'testimonials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_testimonials_id'), 'testimonials', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('testimonials')
    op.drop_table('sectors')
