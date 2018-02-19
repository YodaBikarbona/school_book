"""add_class_student_table

Revision ID: 60065239fafc
Revises: cdfa2bd94504
Create Date: 2018-02-19 11:57:17.399435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60065239fafc'
down_revision = 'cdfa2bd94504'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'classes_student',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('classes_id', sa.Integer, nullable=False),
            sa.Column('student_id', sa.Integer, nullable=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('classes_student')
    except Exception as ex:
        print(ex)
