"""merge migration heads

Revision ID: d593fdad4170
Revises: ('003', 'ddaa1369ece5')
Create Date: 2026-09-25 01:10:22.235225

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "d593fdad4170"
down_revision: Union[str, Sequence[str], None] = (
    "003",
    "ddaa1369ece5",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass