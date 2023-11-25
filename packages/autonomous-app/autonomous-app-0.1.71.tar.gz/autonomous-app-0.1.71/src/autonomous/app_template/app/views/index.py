# Built-In Modules

# external Modules
from flask import Blueprint, render_template, request, session

from autonomous import log
from autonomous.auth import auth_required
from autonomous.auth.autoauth import AutoAuth

index_page = Blueprint("index", __name__)


@index_page.route("/", methods=("GET",))
def index():
    return render_template("index.html")


@index_page.route(
    "/protected",
    methods=(
        "GET",
        "POST",
    ),
)
@auth_required
def protected():
    if request.form:
        session.update(request.json)
    context = {"user": AutoAuth.current_user, **request.json}
    return render_template("index.html", **context)
