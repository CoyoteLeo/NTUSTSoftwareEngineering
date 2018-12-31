from flask import url_for, request, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controller.absract import BaseController
from model.Article import Article
from model.Board import Board
from model.Like import Like


class ArticleController(BaseController):
    @staticmethod
    @login_required
    def new_article(board_id):
        if request.method == 'GET':
            return render_template("article/add.html")
        else:
            title = request.form["title"]
            content = request.form["content"]
            author_id = current_user.id
            article = Article.create(title=title, content=content, author_id=author_id, board_id=board_id)
            if type(article) == str:
                return render_template("article/add.html", error=article)
            return redirect(url_for('article', board_id=board_id, article_id=article.id))

    @staticmethod
    @login_required
    def article(board_id, article_id):
        article = Article.get(id=article_id)
        boards = Board.filter(state=1)
        isLike = Like.exist(article_id=article_id, author_id=current_user.id)
        result = {
            "article": article,
            "boards": boards,
            "isLike": isLike
        }
        if article:
            if request.method == 'GET':
                return render_template("article/view.html", **result)
            if request.method == 'POST' and current_user.id == article.author_id:
                if request.method == 'POST':
                    if request.form.get("delete", None) == "delete":
                        result = article.delete()
                        if type(result) == str:
                            return render_template("article/view.html", error=result, **result)
                        return redirect(f"/board/{board_id}/")
                    elif request.form.get("edit", None) == "edit":
                        return render_template("article/edit.html", **result)
                    else:
                        article.title = request.form["title"]
                        article.content = request.form["content"]
                        article.save()
                        if type(article) == str:
                            return render_template("article/edit.html", error="修改失敗", **result)
                        return render_template("article/view.html", **result)
        else:
            return redirect("/")

    @staticmethod
    @login_required
    def search():
        search = request.form["article_title"]
        result = dict()
        articles = Article.search_for_title(search)
        result["boards"] = Board.filter(state=1)
        if type(articles) == str:
            result["error"] = articles
            result["articles"] = []
        else:
            result["articles"] = articles
        return render_template("board/search_result.html", **result)

    @classmethod
    def setupUrl(cls):
        from app import app
        app.add_url_rule(rule='/board/<int:board_id>/article/', view_func=cls.new_article,
                         methods=["POST", "GET"])
        app.add_url_rule(rule='/board/<int:board_id>/article/<int:article_id>/', view_func=cls.article,
                         methods=["POST", "GET", "DELETE"])
        app.add_url_rule(rule='/article/search/', view_func=cls.search, methods=["POST"])
