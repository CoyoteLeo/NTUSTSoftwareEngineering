import os
from importlib import import_module

from flask import Flask
from flask_login import LoginManager
from model.User import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

controllers = [
    'UserController',
]

app.secret_key = '@fnsopdmfknsjfklvn;andspanadfak;dsf;'
login_manager = LoginManager(app)


@login_manager.user_loader
def user_loader(id):
    return User.get(id=id)


login_manager.login_view = "login"

module_parent = import_module(os.path.join(BASE_DIR, "controller"))
for controller_str in controllers:
    getattr(module_parent, controller_str).setupUrl()

if __name__ == '__main__':
    # app.debug = DEBUG
    app.run()
