#!/usr/bin/python
# -*- coding:utf-8 -*-
"""create friendchip

Revision ID: 0a8c5f39e8d0
Revises: ef508e04acb3
Create Date: 2019-01-02 21:31:24.507543+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from model.BaseModel import update_with_timezone
from model.Friend import FriendLevel

revision = '0a8c5f39e8d0'
down_revision = 'ef508e04acb3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Friend',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('user1_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('user2_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('state', sa.Integer, default=FriendLevel.pending.value, index=True),
    )


def downgrade():
    op.drop_table('Friend')
