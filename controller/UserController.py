from flask import url_for, request, render_template
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.utils import redirect

from controller.absract import BaseController
from app import app
from model.User import User


class UserController(BaseController):
    @staticmethod
    def register():
        if request.method == 'GET':
            return render_template("register.html")
        user = User.create(email=request.form["email"], name=request.form["name"], username=request.form["username"],
                           password=request.form["password"])
        if type(user) == str:
            return render_template("register.html", error=user)
        else:
            return redirect(url_for('login'))

    @staticmethod
    def login():
        if request.method == 'GET':
            return render_template("login.html")
        user = User.get(username=request.form["username"], password=request.form["password"])
        if user:
            login_user(user)
            return redirect(url_for('board_list'))
        else:
            return render_template("login.html", error="登入失敗")

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @staticmethod
    @login_required
    def profile():
        if request.method == 'GET':
            user_id = request.values.get("id", None)
            user = current_user if user_id is None else User.get(id=user_id)
            return render_template("user/page.html", user=user)
        else:
            if request.form.get("edit", None) == "edit":
                return render_template("user/profile.html")
            else:
                if request.form["username"] != current_user.username and User.exist(name=request.form["username"]):
                    return render_template("user/profile.html", error="此帳號已被註冊")
                if request.form["email"] != current_user.email and User.exist(email=request.form["email"]):
                    return render_template("user/profile.html", error="此信箱已被註冊")
                current_user.name = request.form["name"]
                current_user.email = request.form["email"]
                current_user.username = request.form["username"]
                current_user.gender = request.form["gender"]
                current_user.save()
                return render_template("user/page.html", user=current_user)

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/login/', view_func=cls.login, methods=["POST", "GET"])
        app.add_url_rule(rule='/register/', view_func=cls.register, methods=["POST", "GET"])
        app.add_url_rule(rule='/logout/', view_func=cls.logout, methods=["GET"])
        app.add_url_rule(rule='/profile/', view_func=cls.profile, methods=["GET", "POST"])
