#!/usr/bin/python
# -*- coding:utf-8 -*-
"""add user male

Revision ID: ef508e04acb3
Revises: cea2c78d9421
Create Date: 2018-12-31 18:59:03.249551+08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ef508e04acb3'
down_revision = 'cea2c78d9421'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'User',
        sa.Column('gender', sa.String(20), default="")
    )


def downgrade():
    op.add_column(
        'User',
        "gender"
    )
