"""create posts table

Revision ID: 706b43ecaf0c
Revises: 
Create Date: 2023-03-13 17:33:09.990128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '706b43ecaf0c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
