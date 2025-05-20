"""add admin column for users table

Revision ID: fdae9e8e2ed8
Revises: f28bda11e25c
Create Date: 2025-05-16 15:42:16.220504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdae9e8e2ed8'
down_revision: Union[str, None] = 'f28bda11e25c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users",sa.Column("user_role",sa.String(10),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
