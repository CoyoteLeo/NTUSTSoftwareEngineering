from flask import url_for, request
from flask_login import logout_user, login_user
from werkzeug.utils import redirect

from controller.absract import BaseController
from app import app
from model.User import User


class UserController(BaseController):
    @staticmethod
    def login():
        if request.method == 'GET':
            return '''
         <form action='login' method='POST'>
         <input type='text' name='username' id='username' placeholder='email'/>
         <input type='password' name='password' id='password' placeholder='password'/>
         <input type='submit' name='submit'/>
         </form>
                      '''
        user = User.get(username=request.form["username"], password=request.form["password"])
        if user:
            login_user(user)
            return redirect(url_for('index'))

        return redirect(url_for('login'))

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/login', view_func=cls.login, methods=["POST", "GET"])
        app.add_url_rule(rule='/logout', view_func=cls.logout, methods=["GET"])
