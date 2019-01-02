#!/usr/bin/python
# -*- coding:utf-8 -*-
"""ad

Revision ID: c743fa63bbfe
Revises: 52d54f760a93
Create Date: 2019-01-03 00:16:24.773276+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c743fa63bbfe'
down_revision = '52d54f760a93'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'User',
        sa.Column('ad', sa.Boolean, default=True)
    )


def downgrade():
    op.add_column(
        'User',
        "ad"
    )
