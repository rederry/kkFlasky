import unittest
from app import create_app, db
from app.models import User, Role
from flask import url_for
import re


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # self.client 是flask测试客户端对象, 开启cookie可以记住请求上下文
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """
        测试首页
        :return:
        """
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Strange' in response.get_data(as_text=True))  # as_text将data转为Unicode字符串

    def test_register_and_login(self):
        """
        测试用户注册-登录-退出
        :return:
        """
        # 注册新账户
        response = self.client.post(url_for('auth.register'), data={
            'email': 'kangkang@example.com',
            'username': 'kangkang',
            'password': 'dog',
            'password2': 'dog'
        })
        self.assertTrue(response.status_code == 302)

        # 使用新注册的账户登录
        response = self.client.post(url_for('auth.login'), data={
            'email': 'kangkang@example.com',
            'password': 'dog'
        }, follow_redirects=True)
        self.assertTrue(re.search(b'Hello,\s+kangkang!', response.data))
        self.assertTrue(b'You have not confirmed your account yet' in response.data)

        # 发送确认令牌
        user = User.query.filter_by(email='kangkang@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        self.assertTrue(b'You have confirmed your account.' in response.data)

        # 退出登录
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)