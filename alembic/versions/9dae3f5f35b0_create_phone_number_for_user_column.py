"""create phone_number for user column

Revision ID: 9dae3f5f35b0
Revises:
Create Date: 2025-05-31 16:34:51.320620

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9dae3f5f35b0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
