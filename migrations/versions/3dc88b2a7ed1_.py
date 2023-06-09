"""empty message

Revision ID: 3dc88b2a7ed1
Revises: 
Create Date: 2022-10-31 13:33:26.690103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dc88b2a7ed1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Coin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('fullName', sa.String(length=128), nullable=False),
    sa.Column('precision', sa.Integer(), nullable=True),
    sa.Column('confirms', sa.Integer(), nullable=True),
    sa.Column('contractAddress', sa.String(length=128), nullable=True),
    sa.Column('withdrawalMinSize', sa.String(length=128), nullable=False),
    sa.Column('withdrawalMinFee', sa.String(length=128), nullable=False),
    sa.Column('isWithdrawEnabled', sa.Boolean(), nullable=False),
    sa.Column('isDepositEnabled', sa.Boolean(), nullable=False),
    sa.Column('isMarginEnabled', sa.Boolean(), nullable=False),
    sa.Column('isDebitEnabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Coin')
    # ### end Alembic commands ###
