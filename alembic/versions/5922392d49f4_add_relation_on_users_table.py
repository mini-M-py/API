"""add relation on users table

Revision ID: 5922392d49f4
Revises: ca5e1f1ca3e1
Create Date: 2023-03-13 18:09:51.541974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5922392d49f4'
down_revision = 'ca5e1f1ca3e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column('posts', "owner_id")
    pass
