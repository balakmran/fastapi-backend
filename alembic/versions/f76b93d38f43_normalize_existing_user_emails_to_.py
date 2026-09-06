"""normalize existing user emails to lowercase.

Revision ID: f76b93d38f43
Revises: 7dc9a90dcc5a
Create Date: 2026-09-05 20:35:47.133293

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f76b93d38f43"
down_revision: str | Sequence[str] | None = "7dc9a90dcc5a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Lowercase every existing email value.

    The case-insensitive unique index (`f2f495892c21`) enforced
    uniqueness of `lower(email)` going forward but never backfilled
    existing rows. Idempotent, and it cannot violate that index, which
    already rejects two rows differing only by case.
    """
    op.execute("UPDATE users SET email = lower(email)")


def downgrade() -> None:
    """No-op: the original mixed case is not recoverable once lowered."""
