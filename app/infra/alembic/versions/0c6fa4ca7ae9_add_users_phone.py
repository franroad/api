"""add users_phone

Revision ID: 0c6fa4ca7ae9
Revises: 
Create Date: 2025-10-25 21:31:22.596384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c6fa4ca7ae9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.column("phone",sa.int))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users","phone")
