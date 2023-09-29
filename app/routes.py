from werkzeug.security import check_password_hash
from app.models import User
from app import app, db
from app.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверяем, существует ли пользователь с таким именем
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            # Если пользователя с таким именем нет, то создаем нового пользователя
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()

            # Автоматическая авторизация пользователя после регистрации
            login_user(user)

            return redirect(url_for('chat'))
        else:
            flash('Пользователь с таким именем уже существует', 'danger')
    else:
        flash('Пароли не совпадают', 'danger')
        return render_template('register.html', form=form)
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

@app.route('/chat')
def chat():
    return render_template('chat.html', username=current_user.username)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))