"""empty message

Revision ID: b4d6c2a3ee22
Revises: ed0aa865a31c
Create Date: 2019-09-20 07:07:47.819662

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b4d6c2a3ee22'
down_revision = 'ed0aa865a31c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vendor', 'created')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendor', sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
