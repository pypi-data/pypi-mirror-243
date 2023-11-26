import logging
import os

import rq_dashboard
from config import APIConfig
from flask import Flask, url_for
from views.api.task import task_endpoint


def create_api():
    app = Flask(os.getenv("APP_NAME", __name__))
    app.config.from_object(APIConfig)

    #################################################################
    #                             Plug-ins                          #
    #################################################################
    rq_dashboard.web.setup_rq_connection(app)

    ######################################
    #           Blueprints               #
    ######################################
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
    app.register_blueprint(task_endpoint, url_prefix="/task")

    ## Disables the favicon.ico not found error
    @app.route("/favicon.ico")
    def favicon():
        return url_for("static", filename="data:,")

    return app
