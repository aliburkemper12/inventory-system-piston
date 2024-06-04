"""empty message

Revision ID: 1e5fb63a764b
Revises: d04ae15b3e06
Create Date: 2024-06-04 07:38:14.975074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e5fb63a764b'
down_revision = 'd04ae15b3e06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('roles')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('roles', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
