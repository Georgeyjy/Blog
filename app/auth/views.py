from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from app.email import send_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check if the user exists
        user = User.query.filter_by(email=form.email.data).first()
        # check if password correct
        if user and user.verify_password(form.password.data):
            # check if user select 'remember me'
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('邮箱地址或密码有误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '请确认您的邮箱地址', 'auth/email/confirm', user=user, token=token)
        flash('注册成功！一封确认邮件已发至您的邮箱！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('您的邮箱已确认，请直接登录！')
    if current_user.confirm(token):
        flash('邮箱确认成功！请登录！')
    else:
        flash('确认链接失效或已过期，请重新确认！')
    return redirect(url_for('main.index'))
