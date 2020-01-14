"""empty message

Revision ID: 075ef7b7f465
Revises: c8df1e64ac3f
Create Date: 2020-01-14 00:46:47.381666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '075ef7b7f465'
down_revision = 'c8df1e64ac3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test2', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('test2')

    # ### end Alembic commands ###
