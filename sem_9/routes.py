from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import gen_salt, generate_password_hash

from authentication import app, LoginForm, users_by_email, RegisterForm, User, users_by_id


@app.route('/')
def index():
    print(request.args)
    return render_template("index.html")


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = users_by_email.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))
        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register/', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = users_by_email.get(form.username.data)
        if not user:
            salt = gen_salt(100)
            user = User(form.username.data, generate_password_hash(form.password.data + salt), salt)
            users_by_email[form.username.data] = users_by_id[user.get_id()] = user
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))
        flash("User already exists", 'error')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))
