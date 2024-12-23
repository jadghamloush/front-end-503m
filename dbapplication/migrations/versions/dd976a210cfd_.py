"""empty message

Revision ID: dd976a210cfd
Revises: dd2fca4e04d0
Create Date: 2024-11-04 14:14:24.979973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd976a210cfd'
down_revision = 'dd2fca4e04d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accessories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activewear_tops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bottoms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('compression_wear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('footwear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('outerwear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('protective_gear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recovery_and_wellness',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialty_sportswear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('swimwear',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('swimwear')
    op.drop_table('specialty_sportswear')
    op.drop_table('recovery_and_wellness')
    op.drop_table('protective_gear')
    op.drop_table('outerwear')
    op.drop_table('footwear')
    op.drop_table('compression_wear')
    op.drop_table('bottoms')
    op.drop_table('activewear_tops')
    op.drop_table('accessories')
    # ### end Alembic commands ###
