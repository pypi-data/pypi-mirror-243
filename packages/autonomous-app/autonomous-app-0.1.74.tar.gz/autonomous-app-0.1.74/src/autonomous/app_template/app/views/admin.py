# Built-In Modules

# external Modules
from flask import Blueprint, render_template, request, session
from autonomous import log
from autonomous.auth import auth_required

admin_page = Blueprint("admin", __name__)


@admin_page.route("/", methods=("GET",))
@auth_required
def index():
    if request.form:
        session.update(request.form)
    return render_template("admin.html")
