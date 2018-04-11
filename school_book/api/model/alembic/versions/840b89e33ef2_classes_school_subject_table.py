"""classes_school_subject_table

Revision ID: 840b89e33ef2
Revises: 1fc8e8068621
Create Date: 2018-03-13 09:11:22.006921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '840b89e33ef2'
down_revision = '1fc8e8068621'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'classes_school_subject',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('classes_id', sa.Integer, nullable=False),
            sa.Column('school_subject_id', sa.Integer, nullable=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('classes_school_subject')
    except Exception as ex:
        print(ex)
