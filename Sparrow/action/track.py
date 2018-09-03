from dal.models import *
from dal.dao.action_dao import ActionDao
import types
from django.http.request import *


def track(type):
    def decorator(func):
        def wrapper(*args, **kw):
            action = Action()
            action.type = type.value
            action.function_info = func.__name__
            action.request_info = args[0].__str__()

            if args[0].user.id is not None :
                action.user = args[0].user
            ActionDao.add_action(action)
            return func(*args, **kw)

        return wrapper

    return decorator
