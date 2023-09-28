from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))  # В реальном проекте следует хранить пароли в захешированном виде

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return (self.id)