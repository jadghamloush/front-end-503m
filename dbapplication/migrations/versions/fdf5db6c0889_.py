"""empty message

Revision ID: fdf5db6c0889
Revises: 6b3d54ae4beb
Create Date: 2024-11-06 15:46:01.936419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdf5db6c0889'
down_revision = '6b3d54ae4beb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accessories_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('activewear_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('bottoms_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('compression_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('footwear_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('outerwear_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('protective_gear_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('recovery_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('specialty_sportswear_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    with op.batch_alter_table('swimwear_subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('swimwear_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('specialty_sportswear_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('recovery_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('protective_gear_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('outerwear_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('footwear_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('compression_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('bottoms_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('activewear_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('accessories_subcategories', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###