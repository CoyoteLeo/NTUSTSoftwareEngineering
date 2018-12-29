from flask import url_for, request
from controller.absract import BaseController
from model.Article import Article


class ArticleController(BaseController):
    @staticmethod
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
            author_id = 1
            article = Article.create(title=title, content=content, author_id=author_id, board_id=board_id)
            if type(article) == str:
                param = {"error": article}
                return article
            return "success"

    @staticmethod
    def change_article(board_id, article_id):
        if request.method == 'GET':
            return '''
         <form action='' method='POST'>
         <input type='text' name='title' id='title' placeholder='title'/>
         <input type='text' name='content' id='content' placeholder='content'/>
         <input type='submit' name='submit'/>
         </form>
                      '''
        if request.method == 'POST':
            title = request.form["title"]
            content = request.form["content"]
            article = Article.change(title=title, content=content, board_id=board_id, id=article_id)
            if type(article) == str:
                param = {"error": article}
                return article
            return "success"
        else:
            article = Article.delete(id=article_id)
            if type(article) == str:
                param = {"error": article}
                return article
            return "success"

    @classmethod
    def setupUrl(cls):
        from app import app
        app.add_url_rule(rule='/board/<int:board_id>/article/', view_func=cls.new_article,
                         methods=["POST", "GET"])
        app.add_url_rule(rule='/board/<int:board_id>/article/<int:article_id>/', view_func=cls.change_article,
                         methods=["POST", "GET", "DELETE"])
