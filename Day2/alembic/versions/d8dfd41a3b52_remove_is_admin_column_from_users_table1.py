"""Remove is_admin column from users table1

Revision ID: d8dfd41a3b52
Revises: ba6041bc0388
Create Date: 2025-08-03 15:53:46.144565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8dfd41a3b52'
down_revision: Union[str, Sequence[str], None] = 'ba6041bc0388'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'is_admin')

def downgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))