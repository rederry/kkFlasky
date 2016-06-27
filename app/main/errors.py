from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    """
    使用HTTP内容协商处理错误,向web客户端发送json响应,除此之外都发送html响应
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:  # 检查request的首部
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
