"""add role column to users

Revision ID: 64d9f96d4936
Revises: 332b4bb9cbca
Create Date: 2026-02-08 17:15:27.452176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64d9f96d4936'
down_revision: Union[str, Sequence[str], None] = '332b4bb9cbca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='user'))
    op.alter_column('users', 'role', server_default=None)  # optional: remove default after setting values

def downgrade():
    op.drop_column('users', 'role')