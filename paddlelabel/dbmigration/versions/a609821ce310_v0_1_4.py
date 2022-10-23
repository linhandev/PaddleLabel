"""v0.1.4. Add data.predicted

Revision ID: a609821ce310
Revises: 61968cbf48e8
Create Date: 2022-10-22 03:58:11.232173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a609821ce310'
down_revision = '61968cbf48e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('predicted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'predicted')
    # ### end Alembic commands ###
