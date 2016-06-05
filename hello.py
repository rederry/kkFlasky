import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
# web 表单
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
# database
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate,MigrateCommand
# mail
from flask.ext.mail import Mail

# @app.route('/secret')
# @login_required
# def secret():
#     return "Only authenticated users are allowed!"

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.sina.com'
app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)


# web form class
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


# SQLAlchemy classes
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name
    #relationship
    user = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    def __repr__(self):
        return '<User %r>' % self.username
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


# 配置shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# home目录路由
@app.route('/', methods=['GET','POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''

        # if old_name is not None and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')
 
        return redirect(url_for('index'))
    return render_template('index.html',name=session.get('name'),form=form,user_agent=user_agent,current_time=datetime.utcnow(),known = session.get('known',False))


# 用户页面路由
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)


# 错误页面路由
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def intenal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
