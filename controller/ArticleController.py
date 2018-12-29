from flask import url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controller.absract import BaseController
from model.Article import Article


class ArticleController(BaseController):
    @staticmethod
    @login_required
    def new_article(board_id):
        if request.method == 'GET':
            return '''
         <form action='' method='POST'>
         <input type='text' name='title' id='title' placeholder='title'/>
         <input type='text' name='content' id='content' placeholder='content'/>
         <input type='submit' name='submit'/>
         </form>
                      '''
        else:
            title = request.form["title"]
            content = request.form["content"]
            author_id = current_user.id
            article = Article.create(title=title, content=content, author_id=author_id, board_id=board_id)
            if type(article) == str:
                param = {"error": article}
                return article
            return redirect(url_for('article', board_id=board_id, article_id=article.id))

    @staticmethod
    @login_required
    def article(board_id, article_id):
        article = Article.get(id=article_id)
        if article:
            if current_user.id == article.author_id:
                if request.method == 'GET':
                    return f'''
                            <form action='' method='POST'>
                            <input type='text' name='title' id='title' value={article.title} placeholder='title'/>
                            <input type='text' name='content' id='content' value={article.content} placeholder='content'/>
                            <input type='submit' name='submit'/>
                            </form>
                          '''
                elif request.method == 'POST':
                    title = request.form["title"]
                    content = request.form["content"]
                    article = article.update(title=title, content=content)
                    if type(article) == str:
                        param = {"error": article}
                        return article
                    return redirect(url_for("article", board_id=board_id, article_id=article_id))
                else:
                    article = Article.delete(id=article_id)
                    if type(article) == str:
                        param = {"error": article}
                        return article
                    return redirect(f"/board/{board_id}/")
            else:
                return f"<div>{article.title}</div>" \
                    f"<div>{article.content}<div/>"
        else:
            return redirect("/")

    @classmethod
    def setupUrl(cls):
        from app import app
        app.add_url_rule(rule='/board/<int:board_id>/article/', view_func=cls.new_article,
                         methods=["POST", "GET"])
        app.add_url_rule(rule='/board/<int:board_id>/article/<int:article_id>/', view_func=cls.article,
                         methods=["POST", "GET", "DELETE"])
