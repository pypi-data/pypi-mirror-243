# Built-In Modules
from datetime import datetime

# external Modules
from autonomous import log
from autonomous.tasks import AutoTasks
from flask import Blueprint, request

task_endpoint = Blueprint("task", __name__)


@task_endpoint.route("/checktask", methods=("POST",))
def checktask():
    # log(request.json.get("id"))
    task = AutoTasks().get_task(request.json.get("id"))
    log(task.result, task.status)
    return {"status": task.status, **task.result}
