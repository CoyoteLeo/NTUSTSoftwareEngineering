#!/usr/bin/python
# -*- coding:utf-8 -*-
"""create like

Revision ID: cea2c78d9421
Revises: d96bd422cd0a
Create Date: 2018-12-29 19:44:00.554491+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from model.BaseModel import update_with_timezone

revision = 'cea2c78d9421'
down_revision = 'd96bd422cd0a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Like',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), default=update_with_timezone),
        sa.Column('updated_at', sa.DateTime(timezone=True), default=update_with_timezone,
                  onupdate=update_with_timezone),
        sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False),
        sa.Column('article_id', sa.Integer, sa.ForeignKey("Article.id"), nullable=False)
    )


def downgrade():
    op.drop_table('Like')
