from flask import url_for, request, render_template, make_response
from flask_login import logout_user, login_user, current_user, login_required
from werkzeug.utils import redirect

from controller.absract import BaseController
from app import app
from model.Card import Card
from model.Friend import Friend
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
            resp = redirect(request.values.get("next", "/"))
            if not current_user.ad:
                resp.set_cookie('ad', "1")
            return resp
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
            user = current_user if not user_id else User.get(id=user_id) or current_user
            return render_template("user/page.html", user=user, is_friend=user.is_friend)
        else:
            if request.form.get("edit", None) == "edit":
                return render_template("user/profile.html")
            else:
                if request.form["email"] != current_user.email and User.exist(email=request.form["email"]):
                    return render_template("user/profile.html", error="此信箱已被註冊")
                current_user.name = request.form["name"]
                current_user.email = request.form["email"]
                current_user.gender = request.form["gender"]
                current_user.save()
                return render_template("user/page.html", user=current_user)

    @staticmethod
    @login_required
    def friend():
        if request.method == "GET":
            return render_template("user/friends.html", user=current_user)
        if request.form.get("add", None) == "add":
            user_id = int(request.form.get("friend_id"))
            Friend.create(user1_id=current_user.id, user2_id=user_id)
            return redirect(request.referrer)
        elif request.form.get("approve", None) == "approve":
            friend_id = int(request.form.get("friend_id"))
            friend = Friend.get(id=friend_id)
            friend.approve()
            return redirect(request.referrer)
        elif request.form.get("delete", None) == "delete":
            friend_id = int(request.form.get("friend_id"))
            friend = Friend.get(id=friend_id)
            friend.delete()
            return redirect(request.referrer)

    @staticmethod
    @login_required
    def coin():
        if request.method == "GET":
            return render_template("user/coin.html")
        elif request.form.get("spend", None) == "spend":
            current_user.coin_usage += 2
            current_user.ad = not current_user.ad
            current_user.save()
            resp = make_response(render_template("user/coin.html"))
            if current_user.ad:
                resp.set_cookie('ad', "1", expires=0)
            else:
                resp.set_cookie('ad', "1")
            return resp
        elif request.form.get("card", None) == "card":
            current_user.coin_usage += 5
            current_user.save()
            Card.get(user_id=current_user.id).update_target()
            return redirect("/card/")

    @staticmethod
    @login_required
    def card():
        if request.method == "GET":
            card = Card.get(user_id=current_user.id)
            return render_template("user/card.html", card=card)

    @classmethod
    def setupUrl(cls):
        app.add_url_rule(rule='/login/', view_func=cls.login, methods=["POST", "GET"])
        app.add_url_rule(rule='/register/', view_func=cls.register, methods=["POST", "GET"])
        app.add_url_rule(rule='/logout/', view_func=cls.logout, methods=["GET"])
        app.add_url_rule(rule='/profile/', view_func=cls.profile, methods=["GET", "POST"])
        app.add_url_rule(rule='/friend/', view_func=cls.friend, methods=["GET", "POST"])
        app.add_url_rule(rule='/coin/', view_func=cls.coin, methods=["GET", "POST"])
        app.add_url_rule(rule='/card/', view_func=cls.card, methods=["GET"])
