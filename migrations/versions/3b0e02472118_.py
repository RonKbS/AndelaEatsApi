"""empty message

Revision ID: 3b0e02472118
Revises: c67d14d172d5
Create Date: 2018-11-26 15:56:50.104518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

revision = '3b0e02472118'
down_revision = 'c67d14d172d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    rating_type = postgresql.ENUM('meal', 'order', 'engagement', name='rating_type')
    rating_type.create(op.get_bind())

    op.add_column('vendor_ratings', sa.Column('engagement_id', sa.Integer(), nullable=True))
    op.add_column('vendor_ratings', sa.Column('rating_type', sa.Enum('meal', 'order', 'engagement', name='rating_type'), nullable=True))
    op.add_column('vendor_ratings', sa.Column('type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'vendor_ratings', 'vendor_engagements', ['engagement_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vendor_ratings', type_='foreignkey')
    op.drop_column('vendor_ratings', 'type_id')
    op.drop_column('vendor_ratings', 'rating_type')
    op.drop_column('vendor_ratings', 'engagement_id')

    rating_type = postgresql.ENUM('meal', 'order', 'engagement', name='rating_type')
    rating_type.drop(op.get_bind())
    # ### end Alembic commands ###