"""Change helpID to userID

Revision ID: 2bb5b4a47465
Revises: 9cd4b2ac411c
Create Date: 2024-05-12 16:30:15.477618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bb5b4a47465'
down_revision = '9cd4b2ac411c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faqChat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userID', sa.Text(), nullable=False))
        batch_op.drop_column('sessionID')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('faqChat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sessionID', sa.TEXT(), server_default=sa.text('(123)'), nullable=False))
        batch_op.drop_column('userID')

    # ### end Alembic commands ###
