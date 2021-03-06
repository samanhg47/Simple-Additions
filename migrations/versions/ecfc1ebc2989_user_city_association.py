"""user-city association

Revision ID: ecfc1ebc2989
Revises: dbcf6e7a7fe7
Create Date: 2021-10-21 05:52:47.343671

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ecfc1ebc2989'
down_revision = 'dbcf6e7a7fe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('city_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(None, 'user', 'city', ['city_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'city_id')
    # ### end Alembic commands ###
