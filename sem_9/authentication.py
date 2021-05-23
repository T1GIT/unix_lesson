from datetime import datetime
from time import time_ns

from flask_login import UserMixin, LoginManager
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, gen_salt
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

from app import app

users_by_email = dict()
users_by_id = dict()


class User(UserMixin):
    def __init__(self, email, psw_hash, salt):
        self.id = time_ns()
        self.email = email
        self.psw_hash = psw_hash
        self.psw_salt = salt
        self.reg_date = datetime.now()
        self.tasks = dict()

    def get_id(self):
        return self.id

    def check_password(self, raw_psw):
        return check_password_hash(self.psw_hash, raw_psw + self.psw_salt)


class Guest(UserMixin):
    def __init__(self):
        self.id = time_ns()

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id


class LoginForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()


app.config["SECRET_KEY"] = gen_salt(100)


manager = LoginManager(app)


@manager.user_loader
def load_user(user_id):
    user = users_by_id.get(user_id)
    return user if user else Guest()
