"""update the relationships of the water_consumption table

Revision ID: f8f86ca56b74
Revises: 47ec2650237f
Create Date: 2024-02-20 18:08:37.931053

"""

from typing import Sequence, Union

import sqlalchemy as sa  # noqa: F401
from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision: str = "f8f86ca56b74"
down_revision: Union[str, None] = "47ec2650237f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
