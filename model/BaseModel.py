from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import Column, Integer, DateTime, literal
import datetime
import pytz

from model import session, DB_Session

Base = declarative_base()


def flush_when_exception(func, **kwargs):
    try:
        return func(**kwargs)
    except Exception as e:
        session = DB_Session()
        raise e


def update_with_timezone():
    return datetime.datetime.now(pytz.timezone("Asia/Taipei"))


class BaseModel(AbstractConcreteBase, Base):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    _session = None
    id = Column('id', Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column('created_at', DateTime(timezone=True), default=update_with_timezone,
                        onupdate=update_with_timezone)
    updated_at = Column('updated_at', DateTime(timezone=True), default=update_with_timezone,
                        onupdate=update_with_timezone)

    @classmethod
    def create(cls, **kwargs):
        try:
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
            return obj
        except Exception as e:
            session.flush()

    @classmethod
    def get(cls, order_by=None, **kwargs):
        return cls.filter(order_by=order_by, **kwargs).first()

    @classmethod
    def filter(cls, order_by=None, **kwargs):
        result = session.query(cls).filter_by(**kwargs)
        session.commit()
        return result

    @classmethod
    def all(cls):
        return cls.filter()

    @classmethod
    def exist(cls, **kwargs):
        result = session.query(literal(True)).filter(session.query(cls).filter_by(**kwargs).exists()).scalar()
        session.commit()
        return result

    def save(self):
        try:
            session.merge(self)
            session.commit()
        except Exception as e:
            session.flush()

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.flush()
