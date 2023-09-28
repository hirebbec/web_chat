from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/chat'
app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)
socketio = SocketIO(app)
login = LoginManager(app)
login.login_view = 'login'

from app.models import User
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

