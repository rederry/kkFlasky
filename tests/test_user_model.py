import unittest
from app.models import User, Role, AnonymousUser, Permission
from app import create_app, db


class UserModelTestCase(unittest.TestCase):

    """
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(pasword='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
    """
    # 角色和权限测试
    def test_roles_and_permission(self):
        Role.insert_roles()
        u = User(email='jhon@qq.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

