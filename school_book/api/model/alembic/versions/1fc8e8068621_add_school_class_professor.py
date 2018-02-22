"""add_school_class_professor

Revision ID: 1fc8e8068621
Revises: 49ac9947d28d
Create Date: 2018-02-22 14:22:23.478955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fc8e8068621'
down_revision = '49ac9947d28d'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'classes_professor',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('classes_id', sa.Integer, nullable=False),
            sa.Column('professor_id', sa.Integer, nullable=False),
            sa.Column('multiple_professors', sa.Boolean, default=False)
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('classes_professor')
    except Exception as ex:
        print(ex)
