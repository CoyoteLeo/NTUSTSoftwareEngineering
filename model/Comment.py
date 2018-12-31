import sqlalchemy as  sa
from sqlalchemy.orm import relationship

from model.BaseModel import BaseModel


class Comment(BaseModel):
    __tablename__ = 'Comment'
    content = sa.Column('content', sa.Text, nullable=False)
    author_id = sa.Column('author_id', sa.Integer, sa.ForeignKey("User.id"), nullable=False)
    article_id = sa.Column('article_id', sa.Integer, sa.ForeignKey("Article.id"), nullable=False)

    author = relationship('User', foreign_keys='Comment.author_id', backref='comment_author_id')
    article = relationship('Article', foreign_keys='Comment.article_id', backref='comments')
