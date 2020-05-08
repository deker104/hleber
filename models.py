from flask_login import UserMixin

from web import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client = db.relationship('User', backref='orders_given', foreign_keys=[client_id])
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    volunteer = db.relationship('User', backref='orders_taken', foreign_keys=[volunteer_id])
    text = db.Column(db.Text, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, default=False)
