"""change_type_of_subject_name

Revision ID: 49ac9947d28d
Revises: d2bfbee77e50
Create Date: 2018-02-21 18:14:49.208436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49ac9947d28d'
down_revision = 'd2bfbee77e50'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.drop_column('school_subjects', 'name')
        op.add_column('school_subjects', sa.Column('name', sa.Unicode(255), nullable=False))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.add_column('school_subjects', 'name')
    except Exception as ex:
        print(ex)
