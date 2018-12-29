
from flask_login import login_required
from controller.absract import BaseController
from app import app



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


