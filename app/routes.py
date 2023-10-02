from app.models import User, Message
from app import app, db, socketio
from flask_socketio import emit, join_room
from app.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
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
    elif form.password.data != form.confirm_password.data:
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

        # Отправляем сообщение через WebSocket
        room = author  # Используем имя пользователя в качестве имени комнаты
        join_room(room)
        emit('new_message', {'text': text, 'author': author}, room=room)

    return redirect(url_for('chat'))

@socketio.on('send_message')
@login_required
def send_message(data):
    text = data['text']
    author = data['author']

    if text and author:
        message = Message(text=text, author=author)
        db.session.add(message)
        db.session.commit()

        # Отправляем сообщение через WebSocket
        room = author  # Используем имя пользователя в качестве имени комнаты
        join_room(room)
        emit('new_message', {'text': text, 'author': author}, room=room)

@app.route('/chat')
def chat():
    messages = Message.query.all()
    return render_template('chat.html', messages=messages)