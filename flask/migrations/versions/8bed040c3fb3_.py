"""empty message

Revision ID: 8bed040c3fb3
Revises: 15cde5450063
Create Date: 2020-05-10 13:43:44.742335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bed040c3fb3'
down_revision = '15cde5450063'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('region', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'region')
    # ### end Alembic commands ###
