from app.models import User, Message
from app import app, db
from app.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit
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
        if user is None:
            flash('Пользоваетель не найден', 'danger')
        elif user.password != form.password.data:
            flash('Неправильный логин или пароль', 'danger')
        else:
            login_user(user)  # Авторизация пользователя
            return redirect(url_for('chat'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    text = request.form.get('text')
    author = request.form.get('author')

    if text and author:
        message = Message(text=text, author=author)
        db.session.add(message)
        db.session.commit()

    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    messages = Message.query.all()
    return render_template('chat.html', messages=messages)