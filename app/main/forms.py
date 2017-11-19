from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, ValidationError, Regexp, Email
from ..models import User, Role
from flask_pagedown.fields import PageDownField


class NameForm(Form):
    name = StringField('名字？', validators=[Required()])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    """
        EditProfileForm Class
        用户级资料编辑表单
    """
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    """
        管理员资料编辑表单
    """
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Username must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('权限', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        """

        :param user:
        :param args:
        :param kwargs:
        """
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class PostForm(Form):
    """
    发布博客文章表单
    """
    body = PageDownField("在想什么呢？", validators=[Required()])
    submit = SubmitField('提交')


class CommentForm(Form):
    body = StringField('输入评论', validators=[Required()])
    submit = SubmitField('提交')
