"""craete catogory column for book_store

Revision ID: f28bda11e25c
Revises: 492e33153813
Create Date: 2025-05-15 20:54:26.722789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f28bda11e25c'
down_revision: Union[str, None] = '492e33153813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('book_store',sa.Column('category',sa.String(50),nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    pass
