"""create phone_number for user column

Revision ID: 1d1bc48673a3
Revises: 08d17a09d1ae
Create Date: 2025-05-31 16:54:36.793838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d1bc48673a3'
down_revision: Union[str, None] = '08d17a09d1ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
