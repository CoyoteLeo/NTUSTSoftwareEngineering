from enum import Enum
import sqlalchemy as  sa
from flask_login import UserMixin
from model.BaseModel import BaseModel, update_with_timezone


class UserLevel(Enum):
    admin = 1
    staff = 2
    user = 3
    block = -1


class User(BaseModel, UserMixin):
    __tablename__ = 'User'
    name = sa.Column('name', sa.String(100))
    email = sa.Column('email', sa.String(120), index=True, unique=True, nullable=False)
    username = sa.Column('username', sa.String(120), index=True, unique=True, nullable=False)
    password = sa.Column('password', sa.String(120), nullable=False)
    user_level = sa.Column('level', sa.Integer, default=UserLevel.user.value, index=True)
    last_login = sa.Column('last_login', sa.DateTime(timezone=True), default=update_with_timezone,
                           onupdate=update_with_timezone)

    @property
    def is_active(self):
        return self.user_level > 0

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

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
        return super(User, cls).create()

    @classmethod
    def change(cls, new_name, new_email):
        pass