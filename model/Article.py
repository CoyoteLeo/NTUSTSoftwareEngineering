from enum import Enum

import sqlalchemy as  sa
from sqlalchemy.orm import relationship

from model.BaseModel import BaseModel, update_with_timezone


class BoardActiveLevel(Enum):
    deactive = -1
    pending = 0
    active = 1


class Article(BaseModel):
    __tablename__ = 'Article'
    title = sa.Column('name', sa.String(100), nullable=False)
    content = sa.Column('content', sa.Text, nullable=False)
    author_id = sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    board_id = sa.Column('board_id', sa.Integer, sa.ForeignKey("Board.id"), nullable=False)

    author = relationship('User', foreign_keys='User.author_id', backref='article_author_id')
    board = relationship('Board', foreign_keys='Article.board_id', backref='article_board_id')

    @classmethod
    def get_from_board(cls, board_id):
        return super(Article, cls).filter(board_id=board_id)
