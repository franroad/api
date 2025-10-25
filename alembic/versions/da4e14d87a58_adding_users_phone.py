"""adding users_phone

Revision ID: da4e14d87a58
Revises: 
Create Date: 2025-10-25 22:18:05.539678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da4e14d87a58'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("phone",sa.INTEGER, nullable=True))# Usar el tablename de models.py
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","phone")