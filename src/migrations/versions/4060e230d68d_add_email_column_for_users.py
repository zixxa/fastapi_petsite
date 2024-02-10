"""add email column for users

Revision ID: 4060e230d68d
Revises: 3798b2997dee
Create Date: 2024-02-07 11:03:28.534866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4060e230d68d'
down_revision: Union[str, None] = '3798b2997dee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
