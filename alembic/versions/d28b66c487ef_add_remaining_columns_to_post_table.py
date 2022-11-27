"""add remaining columns to post table

Revision ID: d28b66c487ef
Revises: 203ae63debb6
Create Date: 2022-11-26 21:14:22.756522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = 'd28b66c487ef'
down_revision = '203ae63debb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                sa.Column('published', sa.Boolean(), server_default='TRUE',nullable=False))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('post', 'published')
    pass
