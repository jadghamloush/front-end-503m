"""empty message

Revision ID: f353260ae9fd
Revises: 9b4aa60628d3
Create Date: 2024-11-15 14:17:38.319791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f353260ae9fd'
down_revision = '9b4aa60628d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('return_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('return_requests', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
