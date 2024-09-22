"""Change Post schema

Revision ID: 4e441d9e2120
Revises: f2ce64a5120e
Create Date: 2024-09-12 11:23:07.823207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e441d9e2120'
down_revision: Union[str, None] = 'f2ce64a5120e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('title', sa.String(length=255), nullable=False))
    op.create_unique_constraint(None, 'users', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'title')
    # ### end Alembic commands ###
