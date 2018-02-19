"""add_school_subjects

Revision ID: d2bfbee77e50
Revises: 60065239fafc
Create Date: 2018-02-19 12:02:02.967384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2bfbee77e50'
down_revision = '60065239fafc'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'school_subjects',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.Integer, nullable=False),
            sa.Column('professor_id', sa.Integer, nullable=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('school_subjects')
    except Exception as ex:
        print(ex)