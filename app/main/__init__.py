from flask import Blueprint
from ..models import Permission
main = Blueprint('main', __name__)


# 插入Permission类
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


from . import views, errors
