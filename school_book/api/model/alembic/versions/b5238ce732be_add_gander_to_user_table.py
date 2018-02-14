"""add gander to user table

Revision ID: b5238ce732be
Revises: 120ddaa29576
Create Date: 2018-02-14 16:42:22.529691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5238ce732be'
down_revision = '120ddaa29576'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column('user', sa.Column('gender', sa.Unicode(255)))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_column('user', 'gender')
    except Exception as ex:
        print(ex)
