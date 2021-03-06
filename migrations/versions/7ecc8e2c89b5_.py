"""empty message

Revision ID: 7ecc8e2c89b5
Revises: 
Create Date: 2020-05-08 14:45:43.886657

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7ecc8e2c89b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('volunteer_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('users')
    # ### end Alembic commands ###
