from flask import url_for, request, redirect
from flask_login import login_required, current_user

from controller.absract import BaseController
from model.Comment import Comment


class CommentController(BaseController):
    @staticmethod
    @login_required
    def new_comment(board_id, article_id):
        if request.method == 'GET':
            return '''
            <form action='' method='POST'>
            <input type='text' name='content' id='content' placeholder='content'/>
            <input type='submit' name='submit'/>
            </form>
                         '''
        else:
            content = request.form["content"]
            author_id = current_user.id
            comment = Comment.create(content=content, author_id=author_id, article_id=article_id)
            if type(comment) == str:
                param = {"error": comment}
                return comment
            return redirect(url_for("article", board_id=board_id, article_id=article_id))

    @staticmethod
    @login_required
    def comment(board_id, article_id, comment_id):
        comment = Comment.get(id=comment_id)
        if comment:
            if request.method == 'GET':
                return f'''
                <form action='' method='POST'>
                <input type='text' name='content' id='content' value={comment.content} placeholder='content'/>
                <input type='submit' name='submit'/>
                </form>
                <form action='' method='POST'>
                                <input type='submit' name='delete' value="delete"/>
                            </form>
                             '''
            elif request.method == 'POST':
                if request.form.get("delete", None) == "delete":
                    comment.delete()
                    if type(comment) == str:
                        param = {"error": comment}
                        return comment
                    return redirect(url_for("article", board_id=board_id, article_id=article_id))
                else:
                    comment.content = request.form["content"]
                    comment.save()
                    return redirect(url_for("article", board_id=board_id, article_id=article_id))
        else:
            return redirect("/")

    @classmethod
    def setupUrl(cls):
        from app import app
        app.add_url_rule(rule='/board/<int:board_id>/article/<int:article_id>/comment/', view_func=cls.new_comment,
                         methods=["POST", "GET"])
        app.add_url_rule(rule='/board/<int:board_id>/article/<int:article_id>/comment/<int:comment_id>/',
                         view_func=cls.comment,
                         methods=["POST", "GET"])
