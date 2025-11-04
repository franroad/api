"""add foreign key to  posts table

Revision ID: dfc0e25e41ec
Revises: da4e14d87a58
Create Date: 2025-11-04 13:56:50.795890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfc0e25e41ec'
down_revision: Union[str, Sequence[str], None] = 'da4e14d87a58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts_orm', sa.Column('owner_id',sa.String,nullable=True))
   
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts_orm','owner_id')
    pass
