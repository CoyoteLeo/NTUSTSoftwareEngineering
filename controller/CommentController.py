from flask import url_for, request
from controller.absract import BaseController
from model.Comment import Comment


class CommentController(BaseController):
    @staticmethod
    def new_comment(article_id):
        if request.method == 'GET':
            return '''
            <form action='' method='POST'>
            <input type='text' name='content' id='content' placeholder='content'/>
            <input type='submit' name='submit'/>
            </form>
                         '''
        else:
            content = request.form["content"]
            author_id = 1
            comment = Comment.create(content=content, author_id=author_id, article_id=article_id)
            if type(comment) == str:
                param = {"error": comment}
                return comment
            return "success"

    @staticmethod
    def change_comment(article_id, comment_id):
        if request.method == 'GET':
            return '''
            <form action='' method='POST'>
            <input type='text' name='content' id='content' placeholder='content'/>
            <input type='submit' name='submit'/>
            </form>
                         '''
        if request.method == 'POST':
            content = request.form["content"]

            comment = Comment.change(content=content, article_id=article_id, id=comment_id)
            if type(comment) == str:
                param = {"error": comment}
                return comment
            return "success"
        else:
            comment = Comment.delete(id=comment_id)
            if type(comment) == str:
                param = {"error": comment}
                return comment
            return "success"

    @classmethod
    def setupUrl(cls):
        from app import app
        app.add_url_rule(rule='/article/<int:article_id>/comment/', view_func=cls.new_comment,
                         methods=["POST", "GET"])
        app.add_url_rule(rule='/article/<int:article_id>/comment/<int:comment_id>/', view_func=cls.change_comment,
                         methods=["POST", "GET", "DELETE"])
