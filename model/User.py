from enum import Enum
import sqlalchemy as  sa
from flask_login import UserMixin, current_user
from model.BaseModel import BaseModel, update_with_timezone
from model.Friend import Friend


class UserLevel(Enum):
    admin = 3
    staff = 2
    user = 1
    block = -1


class User(BaseModel, UserMixin):
    __tablename__ = 'User'
    name = sa.Column('name', sa.String(100))
    email = sa.Column('email', sa.String(120), index=True, unique=True, nullable=False)
    username = sa.Column('username', sa.String(120), index=True, unique=True, nullable=False)
    password = sa.Column('password', sa.String(120), nullable=False)
    gender = sa.Column('gender', sa.String(20), default="")
    level = sa.Column('level', sa.Integer, default=UserLevel.user.value, index=True)
    coin_usage = sa.Column('coin_usage', sa.Integer, default=0)
    ad = sa.Column('ad', sa.Boolean, default=True)
    last_login = sa.Column('last_login', sa.DateTime(timezone=True), default=update_with_timezone,
                           onupdate=update_with_timezone)

    @property
    def is_friend(self):
        return Friend.get(user1_id=current_user.id, user2_id=self.id) \
               or Friend.get(user2_id=current_user.id, user1_id=self.id)

    @property
    def is_active(self):
        return self.level > 0

    @property
    def is_authenticated(self):
        return self.level > 0

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.level > 1

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    @classmethod
    def create(cls, **kwargs):
        if cls.exist(email=kwargs["email"]):
            return "此信箱已被註冊過了"
        elif cls.exist(username=kwargs["username"]):
            return "此帳號已被註冊過了"
        return super(User, cls).create(**kwargs)
