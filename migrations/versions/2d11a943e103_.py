"""empty message

Revision ID: 2d11a943e103
Revises: 
Create Date: 2020-05-09 09:41:07.926588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d11a943e103'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('positions', sa.Column('currency', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('positions', 'currency')
    # ### end Alembic commands ###
