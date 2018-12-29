import sqlalchemy as  sa
from sqlalchemy.orm import relationship

from model.BaseModel import BaseModel


class Like(BaseModel):
    __tablename__ = 'Like'
    author_id = sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    article_id = sa.Column('article_id', sa.Integer, sa.ForeignKey("Article.id"), nullable=False)

    author = relationship('User', foreign_keys='Like.author_id', backref='like_author_id')
    article = relationship('Article', foreign_keys='Like.article_id', backref='like_article_id')

    @classmethod
    def givelike(cls, author_id, board_id, article_id):
        return "likeee"

    @classmethod
    def deletelike(cls, author_id, board_id, article_id, id):
        return "no likeee"