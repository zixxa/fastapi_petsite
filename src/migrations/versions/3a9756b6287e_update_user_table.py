"""update user table

Revision ID: 3a9756b6287e
Revises: 4060e230d68d
Create Date: 2024-02-08 19:01:22.878306

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3a9756b6287e"
down_revision: Union[str, None] = "4060e230d68d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("email", sa.String(length=50), nullable=False))
    op.alter_column(
        "users", "name", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "users", "surname", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.drop_constraint("users_name_key", "users", type_="unique")
    op.drop_constraint("users_surname_key", "users", type_="unique")
    op.create_unique_constraint(None, "users", ["email"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.create_unique_constraint("users_surname_key", "users", ["surname"])
    op.create_unique_constraint("users_name_key", "users", ["name"])
    op.alter_column(
        "users", "surname", existing_type=sa.VARCHAR(length=50), nullable=True
    )
    op.alter_column("users", "name", existing_type=sa.VARCHAR(length=50), nullable=True)
    op.drop_column("users", "email")
    # ### end Alembic commands ###
