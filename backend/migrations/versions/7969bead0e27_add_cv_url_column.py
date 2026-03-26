"""add cv_url column

Revision ID: 7969bead0e27
Revises: 
Create Date: 2026-03-25 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# --- Identificadores de Revisión Oficiales ---
revision: str = '7969bead0e27'
down_revision: Union[str, None] = None  # Si esta es tu primera migración, déjalo None.
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Operación de actualización:
    1. Intenta eliminar el índice solo si existe para evitar colisiones.
    2. Añade la columna cv_url de forma segura.
    """
    # Usamos bind para verificar la existencia del índice antes de intentar borrarlo
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    indexes = inspector.get_indexes('site_settings')
    index_names = [idx['name'] for idx in indexes]

    if 'ix_site_settings_id' in index_names:
        op.drop_index('ix_site_settings_id', table_name='site_settings')
    
    # Añadimos la columna
    # Nota: Si ya existiera por un error previo, Alembic lanzará un error que capturará el entrypoint.sh
    op.add_column('site_settings', sa.Column('cv_url', sa.String(), nullable=True))


def downgrade() -> None:
    """
    Operación de reversión:
    Elimina la columna y restaura el índice básico.
    """
    op.drop_column('site_settings', 'cv_url')
    
    # Restauramos el índice de forma estándar
    op.create_index('ix_site_settings_id', 'site_settings', ['id'], unique=False)