#!/usr/bin/python
# -*- coding:utf-8 -*-
"""create Article

Revision ID: dc0cd07fb74a
Revises: df4d825cf4c4
Create Date: 2018-12-29 14:51:23.975701+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from model.BaseModel import update_with_timezone

revision = 'dc0cd07fb74a'
down_revision = 'df4d825cf4c4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Article',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('board_id', sa.Integer, sa.ForeignKey("Board.id"), nullable=False),
    )


def downgrade():
    op.drop_table('Article')
