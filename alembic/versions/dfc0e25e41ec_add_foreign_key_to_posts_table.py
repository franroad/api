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
    op.add_column('posts', sa.Column('owner_id',sa.INTEGER,nullable=False)),
    op.create_foreign_key('post_users_fk', source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
