"""craete price column in store

Revision ID: 492e33153813
Revises: 
Create Date: 2025-05-15 19:53:50.477321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '492e33153813'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('book_store',sa.Column('price',sa.String(50),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
