from datetime import datetime

from flask import session, redirect, url_for, render_template, Blueprint

from app import db
from app.main.forms import NameForm
from app.models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', c_time=datetime.utcnow())


@main.route('/user/', methods=['GET', 'POST'])
def user_info():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
    return render_template('user.html', name=session.get('name'), known=session.get('known', False), form=form)
