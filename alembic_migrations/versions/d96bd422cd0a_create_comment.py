#!/usr/bin/python
# -*- coding:utf-8 -*-
"""create comment

Revision ID: d96bd422cd0a
Revises: dc0cd07fb74a
Create Date: 2018-12-29 14:53:54.308404+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from model.BaseModel import update_with_timezone

revision = 'd96bd422cd0a'
down_revision = 'dc0cd07fb74a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Comment',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('article_id', sa.Integer, sa.ForeignKey("Article.id"), nullable=False),

    )


def downgrade():
    op.drop_table('Comment')
