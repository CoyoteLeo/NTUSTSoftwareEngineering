from flask import url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from model.Like import Like
from controller.absract import BaseController


class LikeController(BaseController):
    @staticmethod
    @login_required
    def like(board_id, article_id):
        author_id = current_user.id
        like = Like.get(article_id=article_id, author_id=author_id)
        if like:
            like.delete()
        else:
            Like.create(article_id=article_id, author_id=author_id)
        return redirect(url_for("article", board_id=board_id, article_id=article_id))

    @classmethod
    def setupUrl(cls):
        from app import app
        app.add_url_rule(rule='/board/<int:board_id>/article/<int:article_id>/like/', view_func=cls.like,
                         methods=["POST"])
