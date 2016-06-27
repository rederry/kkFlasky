"""
    API 的修饰器

"""

from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission):
    """
    防止未授权用户创建新博客的修饰器
    :param permission:
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
