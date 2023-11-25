# Built-In Modules

# external Modules
from datetime import datetime, timezone

from flask import Blueprint, redirect, render_template, request, session, url_for

from autonomous import log
from autonomous.auth import AutoUser, GithubAuth, GoogleAuth

auth_page = Blueprint("auth", __name__)


@auth_page.route("/login", methods=("GET", "POST"))
def login():
    # session["user"] = None
    # AutoUser.table().flush_table()
    if session.get("user"):
        if last_login := session["user"]["last_login"]:
            log(last_login)
            diff = datetime.now(timezone.utc) - last_login
            if diff.days <= 30 and session["user"]["state"] == "authenticated":
                return redirect(url_for("index.protected"))

    if request.method == "POST":
        session["user"] = None
        if request.form.get("authprovider") == "google":
            authorizer = GoogleAuth()
            session["authprovider"] = "google"
        elif request.form.get("authprovider") == "github":
            authorizer = GithubAuth()
            session["authprovider"] = "github"
        uri, state = authorizer.authenticate()
        session["authprovider_state"] = state
        # log(uri, state)
        return redirect(uri)

    return render_template("login.html")


@auth_page.route("/authorize", methods=("GET", "POST"))
def authorize():
    # log(request.args)
    if session["authprovider"] == "google":
        authorizer = GoogleAuth()
    elif session["authprovider"] == "github":
        authorizer = GithubAuth()
    response = str(request.url)
    # log(response)
    user_info, token = authorizer.handle_response(
        response, state=request.args.get("state")
    )
    # log(user_info["email"])
    user_info["provider"] = session["authprovider"]
    user = AutoUser.authenticate(user_info, token)
    # log(user)
    session["user"] = user.serialize()
    return redirect(url_for("auth.login"))


@auth_page.route("/logout", methods=("POST", "GET"))
def logout():
    if session.get("user"):
        user = AutoUser.get(session["user"]["pk"])
        user.state = "unauthenticated"
        user.save()
        session.pop("user")
        # log(f"User {user.name} logged out")
    return redirect(url_for("auth.login"))
