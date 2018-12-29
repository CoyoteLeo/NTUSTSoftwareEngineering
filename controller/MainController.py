from flask import url_for, request
from flask_login import logout_user, login_user, login_required
from werkzeug.utils import redirect

from controller.absract import BaseController
from app import app
from model.User import User


class MainController(BaseController):
    @staticmethod
    @login_required
    def index():
        from model.User import User
        # user = User.create(name="123", email="123", username="123", password="123")
        print("stop")
        return 'Hello World!'

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/', view_func=cls.index, methods=["POST", "GET"])


