from enum import Enum

import sqlalchemy as  sa
from sqlalchemy.orm import relationship

from model.BaseModel import BaseModel


class FriendLevel(Enum):
    friend = 1
    pending = 0
    block = -1


class Friend(BaseModel):
    __tablename__ = 'Friend'
    user1_id = sa.Column('user1_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    user2_id = sa.Column('user2_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    state = sa.Column('state', sa.Integer, default=FriendLevel.pending.value, index=True)

    user1 = relationship('User', foreign_keys='Friend.user1_id', backref='friends1')
    user2 = relationship('User', foreign_keys='Friend.user2_id', backref='friends2')

    def approve(self):
        self.state = FriendLevel.friend.value
        self.save()
