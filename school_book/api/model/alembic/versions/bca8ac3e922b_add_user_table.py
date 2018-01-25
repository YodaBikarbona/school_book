"""add_user_table

Revision ID: bca8ac3e922b
Revises: 
Create Date: 2018-01-21 10:45:58.383905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bca8ac3e922b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'user',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('unique_ID', sa.Unicode(255), default=''),
            sa.Column('first_name', sa.Unicode(255), nullable=False),
            sa.Column('last_name', sa.Unicode(255), nullable=False),
            sa.Column('email', sa.Unicode(255), default=''),
            sa.Column('parent_one', sa.Unicode(255), default=''),
            sa.Column('parent_two', sa.Unicode(255), default=''),
            sa.Column('role', sa.Unicode(255), nullable=False),
            sa.Column('activated', sa.Boolean, default=False),
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('user')
    except Exception as ex:
        print(ex)
