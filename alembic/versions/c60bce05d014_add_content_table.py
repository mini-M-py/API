"""add content table

Revision ID: c60bce05d014
Revises: 706b43ecaf0c
Create Date: 2023-03-13 17:49:27.006018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c60bce05d014'
down_revision = '706b43ecaf0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
