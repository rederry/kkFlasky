from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from ..models import AnonymousUser, User
from .errors import unauthorized, forbidden
from . import api
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """
    认证密码接口
    :param email_or_token: 邮箱或者令牌
    :param password:
    :return:
    """
    if email_or_token == '':  # 如果为空便是匿名用户
        g.current_user = AnonymousUser()
        return True
    if password == '':  # 如果密码为空,则提供的是令牌
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()  # 如果两个都不为空则是提供的用户名和密码
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden("Unconfirmed account")


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})
