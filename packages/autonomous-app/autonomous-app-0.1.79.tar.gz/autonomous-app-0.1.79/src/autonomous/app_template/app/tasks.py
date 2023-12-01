import time

from autonomous import log


def mocktask():
    log("MockTask - starting")
    time.sleep(1)
    log("MockTask - complete")
    return "success"


def longmocktask():
    log("LongTask - Starting")
    time.sleep(30)
    log("LongTask - Complete")
    return "success"


def parametermocktask(*args, **kwargs):
    log("ParameterMockTask - Starting", args, kwargs)
    result = args[0] + args[1]
    log("ParameterMockTask - complete", result)
    return result


def errormocktask(a, b):
    time.sleep(2)
    return int(a) + str(b)
