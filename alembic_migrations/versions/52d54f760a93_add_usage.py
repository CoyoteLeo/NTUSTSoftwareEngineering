#!/usr/bin/python
# -*- coding:utf-8 -*-
"""add usage

Revision ID: 52d54f760a93
Revises: 0a8c5f39e8d0
Create Date: 2019-01-02 22:41:27.495384+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52d54f760a93'
down_revision = '0a8c5f39e8d0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'User',
        sa.Column('coin_usage', sa.Integer, default=0)
    )


def downgrade():
    op.add_column(
        'User',
        "coin_usage"
    )
