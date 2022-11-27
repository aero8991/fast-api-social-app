"""add content column to post table

Revision ID: 89a578c126cb
Revises: 031efd062ef7
Create Date: 2022-11-26 19:26:39.162393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a578c126cb'
down_revision = '031efd062ef7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False) )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
