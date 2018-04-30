"""add approve or reject option to absence

Revision ID: adb048541dc8
Revises: fb260fd7c5ee
Create Date: 2018-04-30 14:02:55.651147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adb048541dc8'
down_revision = 'fb260fd7c5ee'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.add_column('absences', sa.Column('approved', sa.Boolean, nullable=True, default=None))
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_column('absences', 'approved')
    except Exception as ex:
        print(ex)
