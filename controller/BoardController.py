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
            return render_template("board/apply_board.html")
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
    def article_list(board_id):
        articles = Article.get_from_board_with_info(board_id=board_id)
        boards = Board.filter(state=1)
        return render_template("board/article_list.html", board_id=board_id, articles=articles, boards=boards)

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/board/', view_func=cls.send_request, methods=["POST", "GET"])
        app.add_url_rule(rule='/board/<int:board_id>/', view_func=cls.article_list, methods=["GET"])
        app.add_url_rule(rule='/', view_func=cls.board_list, methods=["GET"])
