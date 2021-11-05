"""shelter unique constraint

Revision ID: 733be51c7227
Revises: aa4e54542630
Create Date: 2021-11-05 15:08:27.045024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '733be51c7227'
down_revision = 'aa4e54542630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('nameNaddress', 'shelter', ['shelter_name', 'address'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('nameNaddress', 'shelter', type_='unique')
    # ### end Alembic commands ###
