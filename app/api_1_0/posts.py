"""
    用于客户端的post文章逻辑处理
"""

from flask import request, g, jsonify, url_for, current_app
from . import api
from ..models import Post, Permission
from .. import db
from .decorators import permission_required
from .errors import forbidden


@api.route('/posts/')
def get_posts():
    """
    获取分页文章
    :return:
    """
    page = request.args.get('page', 1, type=int)  # 页码信息放在request请求中
    pagination = Post.query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/post/<int:id>')
def get_post(id):
    """
    获取某个id的文章
    :return:
    """
    post = Post.query.get_or_404(id)  # 目前404由程序层响应
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    """
    客户端发布新文章 (得益于错误处理程序的实现,创建过程很直观)
    :return: 201状态码, 并把Location的首部设为刚创建的这个资源的URL(方便客户端操作,客户端无需在发布后再发起一个GET请求)
    """
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/post/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    """
    PUT请求更新现有文章
    :param id:
    :return:
    """
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):  # 保证用户是文章作者或者是管理员
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
