"""add_classes_table

Revision ID: cdfa2bd94504
Revises: 095345111913
Create Date: 2018-02-19 11:51:49.499200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdfa2bd94504'
down_revision = '095345111913'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'classes',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('school_year_id', sa.Integer, nullable=False),
            sa.Column('name', sa.Unicode(255), nullable=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('classes')
    except Exception as ex:
        print(ex)
