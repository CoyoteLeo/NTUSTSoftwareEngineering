from flask import url_for, request, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from controller.absract import BaseController
from app import app
from model.Article import Article
from model.Board import Board


class BoardController(BaseController):
    @staticmethod
    @login_required
    def send_request():
        if request.method == 'GET':
            return '''
         <form action='' method='POST'>
         <input type='text' name='name' id='name' placeholder='name'/>
         <input type='text' name='description' id='description' placeholder='description'/>
         <input type='submit' name='submit'/>
         </form>
                      '''
        else:
            name = request.form["name"]
            description = request.form["description"]
            board = Board.create(name=name, description=description, applier_id=current_user.id)
            if type(board) == str:
                param = {"error": board}
                return board
            return redirect(url_for('board_list'))

    @staticmethod
    @login_required
    def board_list():
        boards = Board.get_list()
        return render_template("board/board_list.html", boards=boards)

    @staticmethod
    @login_required
    def board(board_id):
        articles = Article.filter(board_id=board_id)
        return render_template("board/article_list.html", board_id=board_id, articles=articles)

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/board/', view_func=cls.send_request, methods=["POST", "GET"])
        app.add_url_rule(rule='/board/<int:board_id>/', view_func=cls.board, methods=["GET"])
        app.add_url_rule(rule='/', view_func=cls.board_list, methods=["GET"])
