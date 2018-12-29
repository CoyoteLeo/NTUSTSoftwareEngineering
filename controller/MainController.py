
from flask_login import login_required
from controller.absract import BaseController
from app import app



class MainController(BaseController):
    @staticmethod
    @login_required
    def index():
        return 'Hello World!'

    @classmethod
    def setupUrl(cls):
        pass
        # app.add_url_rule(rule='/', view_func=cls.index, methods=["POST", "GET"])


