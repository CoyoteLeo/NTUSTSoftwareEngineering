from flask import url_for, request
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.utils import redirect

from controller.absract import BaseController
from app import app
from model.User import User


class UserController(BaseController):
    @staticmethod
    def register():
        if request.method == 'GET':
            return '''
         <form action='' method='POST'>
         <input type='text' name='username' id='username' placeholder='username'/>
         <input type='email' name='email' id='email' placeholder='email'/>
         <input type='password' name='password' id='password' placeholder='password'/>
         <input type='submit' name='submit'/>
         </form>
                      '''
        user = User.create(email=request.form["email"], username=request.form["username"],
                           password=request.form["password"])
        if type(user) == str:
            return user
        return redirect(url_for('login'))

    @staticmethod
    def login():
        if request.method == 'GET':
            return '''
         <form action='' method='POST'>
         <input type='text' name='username' id='username' placeholder='username'/>
         <input type='password' name='password' id='password' placeholder='password'/>
         <input type='submit' name='submit'/>
         </form>
         <a href="/register">註冊</a>
                      '''
        user = User.get(username=request.form["username"], password=request.form["password"])
        if user:
            login_user(user)
            return redirect(url_for('board_list'))

        return redirect(url_for('login'))

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @staticmethod
    @login_required
    def profile():
        if request.method == 'GET':
            return f'''
             <form action='' method='POST'>
             <input type='text' name='name' id='name' value={"" if not current_user.name else current_user.name} placeholder='name'/>
             <input type='text' name='email' id='email' value={current_user.email} placeholder='email'/>
             <input type='submit' name='submit'/>
             </form>
                          '''
        else:
            user = User.get(id=current_user.id)
            user.name = request.form["name"]
            user.email = request.form["email"]
            user.save()
            if type(user) == str:
                param = {"error": user}
                return user
            return redirect(url_for("profile"))

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/login', view_func=cls.login, methods=["POST", "GET"])
        app.add_url_rule(rule='/register', view_func=cls.register, methods=["POST", "GET"])
        app.add_url_rule(rule='/logout', view_func=cls.logout, methods=["GET"])
        app.add_url_rule(rule='/user/', view_func=cls.profile, methods=["GET", "POST"])
