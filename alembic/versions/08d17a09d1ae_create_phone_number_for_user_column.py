"""create phone_number for user column

Revision ID: 08d17a09d1ae
Revises: 9dae3f5f35b0
Create Date: 2025-05-31 16:45:03.934539

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "08d17a09d1ae"
down_revision: Union[str, None] = "9dae3f5f35b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(25), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
