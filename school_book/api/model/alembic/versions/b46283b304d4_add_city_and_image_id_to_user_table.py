"""add city and image_id to user table

Revision ID: b46283b304d4
Revises: 119ec9393a70
Create Date: 2018-02-14 16:25:48.755383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b46283b304d4'
down_revision = '119ec9393a70'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column('user', sa.Column('city', sa.Unicode(255)))
        op.add_column('user', sa.Column('image_id', sa.Integer()))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_column('user', 'city')
        op.drop_column('user', 'image_id')
    except Exception as ex:
        print(ex)
