"""Remove is_admin column from users table

Revision ID: ba6041bc0388
Revises: 39fd62c78250
Create Date: 2025-08-03 15:50:58.158957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba6041bc0388'
down_revision: Union[str, Sequence[str], None] = '39fd62c78250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('users', 'is_admin')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
