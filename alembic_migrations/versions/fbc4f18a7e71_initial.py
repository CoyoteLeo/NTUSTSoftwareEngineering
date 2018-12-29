"""'initial'

Revision ID: fbc4f18a7e71
Revises: 
Create Date: 2018-12-23 23:21:52.169801

"""
import sqlalchemy as sa
from alembic import op
from model.User import UserLevel
from model.BaseModel import update_with_timezone

# revision identifiers, used by Alembic.
revision = 'fbc4f18a7e71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'User',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('name', sa.String(100)),
        sa.Column('email', sa.String(120), index=True, unique=True, nullable=False),
        sa.Column('username', sa.String(120), index=True, unique=True, nullable=False),
        sa.Column('password', sa.String(120), nullable=False),
        sa.Column('level', sa.Integer, default=UserLevel.user.value, index=True, nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
    )


def downgrade():
    op.drop_table('User')
