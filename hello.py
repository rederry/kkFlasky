from flask import Flask, request, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

#web form class
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

#home目录路由
@app.route('/', methods=['GET','POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html',name=name,form=form,user_agent=user_agent,current_time=datetime.utcnow())

#用户页面路由
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

#错误页面路由
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def intenal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
