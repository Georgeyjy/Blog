from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.auth.forms import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm
from app.models import User
from app.email import send_email

auth = Blueprint('auth', __name__)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and not request.path.startswith('/auth') \
            and not request.path.startswith('/static'):
        return render_template('auth/unconfirmed.html')


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
        flash('您的邮箱已确认，无需重复确认。')
    elif current_user.confirm(token):
        flash('邮箱确认成功！')
    else:
        flash('确认链接失效或已过期，请重新确认！')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '请确认您的邮箱地址', 'auth/email/confirm', user=current_user, token=token)
    flash('一封确认邮件已发至您的邮箱！')
    return redirect(url_for('main.index'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # current_user is an AnonymousUserMixin object, which has no attributes of User instances
            # that are UserMixin objects
            token = user.generate_reset_token()
            send_email(user.email, '重置密码', 'auth/email/reset_password', user=user, token=token)
            flash('一封包含密码重置邮件的链接已发送至您的邮箱！')
            return redirect(url_for('auth.login'))
        else:
            flash('未找到对应的用户！')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('重置密码成功，请登录！')
            return redirect(url_for('auth.login'))
        else:
            flash('重置密码失败！')
    return render_template('auth/change_password.html', form=form)
