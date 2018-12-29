from importlib import import_module

from flask import Flask
from flask_login import LoginManager
from env_production import DEBUG
from model.User import User

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

module_parent = import_module("controller")
for controller_str in controllers:
    getattr(module_parent, controller_str).setupUrl()

if __name__ == '__main__':
    # app.debug = DEBUG
    app.run()
