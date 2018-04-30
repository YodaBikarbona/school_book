"""add_new_table_to_close_subject

Revision ID: fb260fd7c5ee
Revises: 0a9570b8ecce
Create Date: 2018-04-30 11:59:38.681287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb260fd7c5ee'
down_revision = '0a9570b8ecce'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'class_student_subject',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('class_id', sa.Integer, nullable=False),
            sa.Column('school_subject_id', sa.Integer, nullable=False),
            sa.Column('professor_id', sa.Integer, default=False),
            sa.Column('student_id', sa.Integer, nullable=False),
            sa.Column('closed', sa.Boolean, nullable=False),
            sa.Column('grade', sa.Integer)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('class_student_subject')
    except Exception as ex:
        print(ex)
