from werkzeug.security import check_password_hash
from app.models import User
from app import app, db
from app.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))  # Перенаправление на главную страницу после регистрации
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Ваш код проверки логина и пароля
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)  # Авторизация пользователя
            return redirect(url_for('index'))
        else:
            flash('Неправильный логин или пароль', 'danger')
    return render_template('login.html', form=form)