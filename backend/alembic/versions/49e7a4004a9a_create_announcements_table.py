"""create announcements table

Revision ID: 49e7a4004a9a
Revises: eeb476b53482
Create Date: 2026-09-01 18:35:27.484+05:30
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "49e7a4004a9a"
down_revision = "eeb476b53482"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "announcements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "published",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("announcements")
