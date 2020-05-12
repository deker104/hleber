"""empty message

Revision ID: 2f5a27c9032e
Revises: 14caf389c8bb
Create Date: 2020-05-12 02:43:42.742229

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2f5a27c9032e'
down_revision = '14caf389c8bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('notify', sa.Boolean(), nullable=True))
    op.drop_column('users', 'is_linked')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_linked', sa.BOOLEAN(), nullable=True))
    op.drop_column('users', 'notify')
    # ### end Alembic commands ###