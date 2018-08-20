import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '!@#$%54321'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/myblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[THE BLOG]'
    MAIL_SENDER = 'BlogAdmin <george_yjy@163.com>'

    @staticmethod
    def init_app(app):
        pass
