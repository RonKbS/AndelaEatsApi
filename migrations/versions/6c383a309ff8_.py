"""empty message

Revision ID: 6c383a309ff8
Revises: 8dff842c714a
Create Date: 2019-08-14 12:01:43.066719

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '6c383a309ff8'
down_revision = '8dff842c714a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu_template',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.String(
                        length=100), nullable=False),
                    sa.Column('location_id', sa.Integer(), nullable=True),
                    sa.Column('meal_period', ENUM(
                        'lunch', 'breakfast', name="mealperiods", create_type=False), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['location_id'], ['locations.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('menu_template_weekday',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('day', sa.Enum('monday', 'tuesday', 'wednesday',
                                             'thursday', 'friday', name='weekdays'), nullable=False),
                    sa.Column('template_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['template_id'], ['menu_template.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('menu_template_item',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('is_deleted', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.Column('main_meal_id', sa.Integer(), nullable=False),
                    sa.Column('allowed_side', sa.Integer(), nullable=True),
                    sa.Column('allowed_protein', sa.Integer(), nullable=True),
                    sa.Column('day_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['day_id'], ['menu_template_weekday.id'], ),
                    sa.ForeignKeyConstraint(
                        ['main_meal_id'], ['meal_items.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('menu_template_items_to_meal_items',
                    sa.Column('meal_item_id', sa.Integer(), nullable=True),
                    sa.Column('menu_template_item_id',
                              sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['meal_item_id'], ['meal_items.id'], ),
                    sa.ForeignKeyConstraint(['menu_template_item_id'], [
                        'menu_template_item.id'], )
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu_template_items_to_meal_items')
    op.drop_table('menu_template_item')
    op.drop_table('menu_template_weekday')
    op.drop_table('menu_template')
    # ### end Alembic commands ###