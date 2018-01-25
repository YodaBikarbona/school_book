"""add_psw_and_salt_to_user_table

Revision ID: 7696005602e9
Revises: dcc6ab9bdab8
Create Date: 2018-01-22 13:48:05.330514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7696005602e9'
down_revision = 'dcc6ab9bdab8'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column('user', sa.Column('password', sa.Unicode(255), nullable=False))
        op.add_column('user', sa.Column('salt', sa.Unicode(255), nullable=False))
        op.drop_column('user', 'role')
        op.add_column('user', sa.Column('role_id', sa.Integer, nullable=False))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_column('user', 'password')
        op.drop_column('user', 'salt')
        op.drop_column('user', 'role_id')
        op.add_column('user', sa.Column('role', sa.Integer, nullable=False))
    except Exception as ex:
        print(ex)
