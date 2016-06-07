from flask import render_template, session, redirect, url_for, request, abort
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User


# 主页
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           name=session.get('name'),
                           form=form,
                           current_time=datetime.utcnow(),
                           known=session.get('known', False),
                           user_agent=request.headers.get('User-Agent'))


# 用户资料页
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
