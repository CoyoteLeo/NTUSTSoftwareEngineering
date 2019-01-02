#!/usr/bin/python
# -*- coding:utf-8 -*-
"""create card

Revision ID: 24bad376e4e5
Revises: c743fa63bbfe
Create Date: 2019-01-03 02:12:16.082391+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from model.BaseModel import update_with_timezone

revision = '24bad376e4e5'
down_revision = 'c743fa63bbfe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Card',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('target_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    )


def downgrade():
    op.drop_table('Card')
