"""add_user_role

Revision ID: dcc6ab9bdab8
Revises: bca8ac3e922b
Create Date: 2018-01-21 10:56:30.867740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcc6ab9bdab8'
down_revision = 'bca8ac3e922b'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'role',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('role_name', sa.Unicode(255), nullable=False),
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('role')
    except Exception as ex:
        print(ex)
