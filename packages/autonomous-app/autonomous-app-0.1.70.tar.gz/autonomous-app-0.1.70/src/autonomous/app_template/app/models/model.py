from autonomous import log
from autonomous.model import AutoModel, AutoAttribute


class Model(AutoModel):
    # set model default attributes
    attributes = {
        "name": AutoAttribute("TEXT", default=""),
        "age": None,
    }
