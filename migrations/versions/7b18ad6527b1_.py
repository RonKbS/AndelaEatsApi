"""empty message

Revision ID: 7b18ad6527b1
Revises: 42e61807095f
Create Date: 2019-01-21 15:55:06.755228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b18ad6527b1'
down_revision = '42e61807095f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendor_ratings', sa.Column('service_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vendor_ratings', 'service_date')
    # ### end Alembic commands ###
