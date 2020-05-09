import datetime

from flask_login import UserMixin

from app import db
from app import login_manager

__doc__ = """Модуль таблиц БД в виде объектов SQLAlchemy"""


class User(db.Model, UserMixin):
    """Таблица пользователей"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    """Получение объекта пользователя по id (нужно для работы flask-login)"""
    return User.query.get(user_id)


class Order(db.Model):
    """Таблица заказов"""
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client = db.relationship('User', backref='orders_given', foreign_keys=[client_id])
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    volunteer = db.relationship('User', backref='orders_taken', foreign_keys=[volunteer_id])
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    text = db.Column(db.Text, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False)
    client_confirm = db.Column(db.Boolean, default=False)
    volunteer_confirm = db.Column(db.Boolean, default=False)
