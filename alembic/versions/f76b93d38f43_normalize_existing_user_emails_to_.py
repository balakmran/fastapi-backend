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

    The case-insensitive unique index (`f2f495892c21`) enforces
    uniqueness of `lower(email)` going forward, but never backfilled
    existing rows, so a row written before that migration (or before
    `UserBase`'s `field_validator` started normalising on write) could
    still hold mixed-case characters. `UserRepository.get_by_email` now
    compares via `lower(email)` regardless, but this backfill keeps the
    stored value itself consistent with every row created since.

    Safe to run unconditionally and idempotent: only the byte case of
    already-lowercase values is touched, so re-running this migration
    is a no-op. It cannot violate the unique index, because the index
    is already defined over `lower(email)` — two rows differing only
    by case are already rejected as duplicates today, exactly as they
    would be if the column were lowercased from the start.
    """
    op.execute("UPDATE users SET email = lower(email)")


def downgrade() -> None:
    """No-op: the original mixed case is not recoverable once lowered."""
