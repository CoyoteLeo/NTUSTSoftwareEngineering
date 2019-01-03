import datetime
import random
from enum import Enum

import pytz
import sqlalchemy as sa
from flask_login import current_user
from sqlalchemy import not_
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import count

from model import DB_Session
from model.BaseModel import BaseModel
from model.User import User

session = DB_Session()


class Card(BaseModel):
    __tablename__ = 'Card'
    user_id = sa.Column('user_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    target_id = sa.Column('target_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)

    user = relationship('User', foreign_keys='Card.user_id', backref='card_users')
    target = relationship('User', foreign_keys='Card.target_id', backref='card_targets')

    def update_target(self):
        total = session.query(count(User.id).label("count")).select_from(User).first().count - 2
        target = session.query(User) \
            .filter(User.id != current_user.id) \
            .offset(random.randint(0, total)) \
            .limit(1) \
            .first()
        self.target_id = target.id
        self.save()

    @classmethod
    def get(cls, order_by=None, **kwargs):
        instance = cls.filter(order_by=order_by, **kwargs).first()
        if not instance:
            total = session.query(count(User.id).label("count")).select_from(User).first().count - 2
            target = session.query(User) \
                .filter(User.id != current_user.id) \
                .offset(random.randint(0, total)) \
                .limit(1) \
                .first()
            instance = cls(user_id=current_user.id, target_id=target.id)
            instance.update_target()
            return instance
        if ((instance.updated_at + datetime.timedelta(days=1))
            - datetime.datetime.now(pytz.timezone("Asia/Taipei"))).seconds >= 86400:
            instance.update_target()
        return instance
