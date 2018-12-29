#!/usr/bin/python
# -*- coding:utf-8 -*-
"""create board

Revision ID: df4d825cf4c4
Revises: fbc4f18a7e71
Create Date: 2018-12-24 23:00:06.886430+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from model.BaseModel import update_with_timezone
from model.Board import BoardActiveLevel

revision = 'df4d825cf4c4'
down_revision = 'fbc4f18a7e71'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Board',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('admin_id', sa.Integer, sa.ForeignKey("User.id"), nullable=True),
        sa.Column('applier_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('last_active', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('state', sa.Integer, default=BoardActiveLevel.pending.value, nullable=False)
    )


def downgrade():
    op.drop_table('Board')
