import os
from functools import wraps
from importlib import import_module

from flask import Flask, request, current_app
from flask_login import LoginManager, current_user
from flask_login.config import EXEMPT_METHODS

from model.User import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

controllers = [
    'MainController',
    'UserController',
    'BoardController',
    'ArticleController',
    'CommentController',
    'LikeController'
]

app.secret_key = '@fnsopdmfknsjfklvn;andspanadfak;dsf;'
login_manager = LoginManager(app)


@login_manager.user_loader
def user_loader(id):
    return User.get(id=id)

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


login_manager.login_view = "login"

for controller_str in controllers:
    module = import_module(f"controller.{controller_str}")
    getattr(module, controller_str).setupUrl()

if __name__ == '__main__':
    # app.debug = DEBUG
    app.run()
