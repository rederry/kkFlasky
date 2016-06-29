from selenium import webdriver
import unittest
from app import create_app, db
from app.models import User, Role, Post
import threading
import time
import re


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # 启动firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # 如果无法启动浏览器,则跳过测试
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # 禁止日志
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # 创建虚拟数据库
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # 添加管理员
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='kangkang@example.com',
                         username='kangkang', password='dog',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # 在一个线程中启动flask服务器
            threading.Thread(target=cls.app.run).start()

            # 给服务器1秒钟确保开启
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # 关闭服务器和浏览器
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # 销毁数据库
            db.drop_all()
            db.session.remove()

            # 移除(pop)应用上下文
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # 导航到首页
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Strange!', self.client.page_source))

        # 导航到登录页
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login<h1>' in self.client.page_source)

        # 登录
        self.client.find_element_by_name('email').send_keys('kangkang@example.com')
        self.client.find_element_by_name('password').send_keys('dog')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+kangkang!', self.client.page_source))

        # 到用户资料页
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>kangkang<h1>' in self.client.page_source)
