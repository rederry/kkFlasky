from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User



class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])

    username = StringField('用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                     'Username must have only letters,'
                                                                                     'numbers, dots or underscores')])
    password = PasswordField('密码', validators=[Required(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更新密码')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更新密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知邮箱')

