from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import Column, Integer, DateTime, literal
import datetime
import pytz

from model import session

Base = declarative_base()


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
        obj = cls(**kwargs)
        from model import DB_Session
        seesion = DB_Session
        session.add(obj)
        session.commit()
        session.close()
        return obj

    @classmethod
    def get(cls, order_by=None, **kwargs):
        return cls.filter(order_by=order_by, **kwargs).first()

    @classmethod
    def filter(cls, order_by=None, **kwargs):
        from model import session
        return session.query(cls).filter_by(**kwargs)

    @classmethod
    def all(cls):
        return cls.filter()

    @classmethod
    def exist(cls, **kwargs):
        return session.query(literal(True)).filter(session.query(cls).filter_by(**kwargs).exists()).scalar()

    def update(self):
        from model import session
        session.merge(self)

    def delete(self):
        from model import session
        session.delete(self)
        session.close()

# # 5. 查询数据
# # 5.1 返回结果集的第二项
# user = session.query(User).get(2)
#
# # 5.2 返回结果集中的第2-3项
# users = session.query(User)[1:3]
#
# # 5.3 查询条件
# user = session.query(User).filter(User.id < 6).first()
#
# # 5.4 排序
# users = session.query(User).order_by(User.name)
#
# # 5.5 降序（需要导入desc方法）
# from sqlalchemy import desc
#
# users = session.query(User).order_by(desc(User.name))
#
# # 5.6 只查询部分属性
# users = session.query(User.name).order_by(desc(User.name))
# for user in users:
#     print
#     user.name
#
# # 5.7 给结果集的列取别名
# users = session.query(User.name.label('user_name')).all()
# for user in users:
#     print
#     user.user_name
#
# # 5.8 去重查询（需要导入distinct方法）
# from sqlalchemy import distinct
#
# users = session.query(distinct(User.name).label('name')).all()
#
# # 5.9 统计查询
# user_count = session.query(User.name).order_by(User.name).count()
# age_avg = session.query(func.avg(User.age)).first()
# age_sum = session.query(func.sum(User.age)).first()
#
# # 5.10 分组查询
# users = session.query(func.count(User.name).label('count'), User.age).group_by(User.age)
# for user in users:
#     print
#     'age:{0}, count:{1}'.format(user.age, user.count)
#
# # 6.1 exists查询(不存在则为~exists())
# from sqlalchemy.sql import exists
#
# session.query(User.name).filter(~exists().where(User.role_id == Role.id))
# # SELECT name AS users_name FROM users WHERE NOT EXISTS (SELECT * FROM roles WHERE users.role_id = roles.id)
