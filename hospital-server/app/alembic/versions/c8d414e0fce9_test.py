"""Test

Revision ID: c8d414e0fce9
Revises: 
Create Date: 2022-12-17 00:41:37.081523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8d414e0fce9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('child', sa.Column('test', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('child', 'test')
    # ### end Alembic commands ###
