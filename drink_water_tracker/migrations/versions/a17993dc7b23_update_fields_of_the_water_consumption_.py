"""update fields of the water_consumption table

Revision ID: a17993dc7b23
Revises: aa29620e7b8e
Create Date: 2024-02-21 00:24:45.041595

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a17993dc7b23"
down_revision: Union[str, None] = "aa29620e7b8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "water_consumption", sa.Column("drink_date", sa.DateTime(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("water_consumption", "drink_date")
    # ### end Alembic commands ###
