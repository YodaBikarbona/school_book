"""add new attributes to user

Revision ID: 119ec9393a70
Revises: 7696005602e9
Create Date: 2018-02-13 12:36:30.257601

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


def now():
    return datetime.utcnow()


# revision identifiers, used by Alembic.
revision = '119ec9393a70'
down_revision = '7696005602e9'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column('user', sa.Column('created', sa.DateTime()))
        op.add_column('user', sa.Column('first_login', sa.DateTime()))
        op.add_column('user', sa.Column('last_login', sa.DateTime()))
        op.add_column('user', sa.Column('address', sa.Unicode(255), nullable=True))
        op.add_column('user', sa.Column('phone', sa.Unicode(255), nullable=True))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_column('user', 'created')
        op.drop_column('user', 'first_login')
        op.drop_column('user', 'last_login')
        op.drop_column('user', 'address')
        op.drop_column('user', 'phone')
    except Exception as ex:
        print(ex)
