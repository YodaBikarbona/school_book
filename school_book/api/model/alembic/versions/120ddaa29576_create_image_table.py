"""create_image_table

Revision ID: 120ddaa29576
Revises: b46283b304d4
Create Date: 2018-02-14 16:29:08.976933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120ddaa29576'
down_revision = 'b46283b304d4'
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.create_table(
            'image',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.Unicode(255)),
            sa.Column('type', sa.Unicode(255)),
            sa.Column('file_name', sa.Unicode(255))
        )
    except Exception as ex:
        print(ex)


def downgrade():
    try:
        op.drop_table('image')
    except Exception as ex:
        print(ex)
