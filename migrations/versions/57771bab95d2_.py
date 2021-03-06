"""empty message

Revision ID: 57771bab95d2
Revises: 173fd23ed6f4
Create Date: 2019-04-17 12:48:19.898410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57771bab95d2'
down_revision = '173fd23ed6f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'user_roles', ['user_type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'user_type_id')
    # ### end Alembic commands ###
