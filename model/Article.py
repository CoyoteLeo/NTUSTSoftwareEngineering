from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from model import DB_Session
from model.BaseModel import BaseModel
from model.Comment import Comment
from model.Like import Like

session = DB_Session()


class BoardActiveLevel(Enum):
    deactive = -1
    pending = 0
    active = 1


class Article(BaseModel):
    __tablename__ = 'Article'
    title = sa.Column('title', sa.String(100), nullable=False)
    content = sa.Column('content', sa.Text, nullable=False)
    author_id = sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    board_id = sa.Column('board_id', sa.Integer, sa.ForeignKey("Board.id"), nullable=False)

    author = relationship('User', foreign_keys='Article.author_id', backref='articles')
    board = relationship('Board', foreign_keys='Article.board_id', backref='article_board_id')

    @classmethod
    def get_from_board(cls, board_id):
        return super(Article, cls).filter(board_id=board_id)

    @classmethod
    def search_for_title(cls, title):
        result = session.query(Article).filter(Article.title.contains(title))
        return result

    def delete(self, **kwargs):
        Like.filter(article_id=self.id).delete()
        Comment.filter(article_id=self.id).delete()
        super(Article, self).delete()
