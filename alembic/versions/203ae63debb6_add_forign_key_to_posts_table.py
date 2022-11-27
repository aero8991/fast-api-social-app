"""add forign-key to posts table

Revision ID: 203ae63debb6
Revises: 3944b3eeda38
Create Date: 2022-11-26 20:05:15.414586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '203ae63debb6'
down_revision = '3944b3eeda38'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                             local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    
    pass
