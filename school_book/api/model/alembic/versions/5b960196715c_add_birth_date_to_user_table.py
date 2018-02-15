"""add birth date to user table

Revision ID: 5b960196715c
Revises: b5238ce732be
Create Date: 2018-02-15 20:20:02.026283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b960196715c'
down_revision = 'b5238ce732be'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column('user', sa.Column('birth_date', sa.DateTime()))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_column('user', 'birth_date')
    except Exception as ex:
        print(ex)
