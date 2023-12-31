"""delete column TestColumn on table product

Revision ID: 47f9ab5a4820
Revises: 20bda733960d
Create Date: 2023-08-29 16:30:27.622718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47f9ab5a4820'
down_revision = '20bda733960d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('test_column')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test_column', sa.VARCHAR(length=200), nullable=True))

    # ### end Alembic commands ###
