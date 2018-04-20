"""add_grade_table

Revision ID: 0a9570b8ecce
Revises: d944087ca4b9
Create Date: 2018-04-20 14:00:04.861466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a9570b8ecce'
down_revision = 'd944087ca4b9'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'grades',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('class_id', sa.Integer, nullable=False),
            sa.Column('school_subject_id', sa.Integer, nullable=False),
            sa.Column('professor_id', sa.Integer, default=False),
            sa.Column('student_id', sa.Integer, nullable=False),
            sa.Column('date', sa.DateTime(), nullable=False),
            sa.Column('comment', sa.Unicode(255)),
            sa.Column('grade', sa.Integer, nullable=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('grades')
    except Exception as ex:
        print(ex)
