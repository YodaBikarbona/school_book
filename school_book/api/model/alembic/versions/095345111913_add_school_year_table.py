"""add school year table

Revision ID: 095345111913
Revises: 5b960196715c
Create Date: 2018-02-19 10:21:26.569844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '095345111913'
down_revision = '5b960196715c'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'school_year',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('start', sa.Integer, nullable=False),
            sa.Column('end', sa.Integer, nullable=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('school_year')
    except Exception as ex:
        print(ex)
