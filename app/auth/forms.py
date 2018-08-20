from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo
from wtforms import ValidationError

from app.models import User


class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegisterForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                              '用户名应由字母、数字、下划线组成，且不能由数字开头')])
    password = PasswordField(u'密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不匹配！')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'此邮箱已被注册！')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'此用户名已存在！')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField(u'确认')


class PasswordResetForm(FlaskForm):
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码不匹配！')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'确认修改')
