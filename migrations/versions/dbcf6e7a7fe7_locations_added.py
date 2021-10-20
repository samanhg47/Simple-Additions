"""locations added

Revision ID: dbcf6e7a7fe7
Revises: c538e07808c3
Create Date: 2021-10-20 12:16:31.546616

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dbcf6e7a7fe7'
down_revision = 'c538e07808c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('state',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('state_name', sa.String(length=25), nullable=False),
    sa.Column('shorthand', sa.String(length=3), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shorthand')
    )
    op.create_table('city',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('city_name', sa.String(length=150), nullable=False),
    sa.Column('state_name', sa.String(length=25), nullable=False),
    sa.Column('state_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('zipcode', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.DECIMAL(precision=11, scale=6), nullable=False),
    sa.Column('longitude', sa.DECIMAL(precision=11, scale=6), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('city')
    op.drop_table('state')
    # ### end Alembic commands ###
