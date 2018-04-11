"""new_table_absences

Revision ID: d944087ca4b9
Revises: 840b89e33ef2
Create Date: 2018-04-11 19:12:09.225699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd944087ca4b9'
down_revision = '840b89e33ef2'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'absences',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('class_id', sa.Integer, nullable=False),
            sa.Column('school_subject_id', sa.Integer, nullable=False),
            sa.Column('professor_id', sa.Integer, default=False),
            sa.Column('student_id', sa.Integer, nullable=False),
            sa.Column('date', sa.DateTime(), nullable=False),
            sa.Column('comment', sa.Unicode(255))
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('absences')
    except Exception as ex:
        print(ex)
