from enum import Enum

import sqlalchemy as  sa
from flask import request
from sqlalchemy.orm import relationship

from model.BaseModel import BaseModel, update_with_timezone


class BoardActiveLevel(Enum):
    deactive = -1
    pending = 0
    active = 1


class Board(BaseModel):
    __tablename__ = 'Board'
    name = sa.Column('name', sa.String(100), nullable=False)
    description = sa.Column('description', sa.Text, nullable=True)
    admin_id = sa.Column('admin_id', sa.Integer, sa.ForeignKey("User.id"), nullable=True)
    applier_id = sa.Column('applier_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    last_active = sa.Column('last_active', sa.DateTime(timezone=True), default=update_with_timezone,
                            onupdate=update_with_timezone)
    state = sa.Column('state', sa.Integer, default=BoardActiveLevel.pending.value, nullable=False)
    admin = relationship('User', foreign_keys='Board.admin_id', backref='board_id')

    @classmethod
    def create(cls, **kwargs):
        if cls.exist(name=kwargs["name"]):
            return "此版名已使用過"
        return super(Board, cls).create(**kwargs)

    def approve(self):
        self.state = BoardActiveLevel.active.value
        return super(Board, self).update()

    @classmethod
    def get_list(cls):
        return super(Board, cls).filter(state=1)
