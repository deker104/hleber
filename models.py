# from web import db
import sqlalchemy as db
from db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order = db.Column(db.String, nullable=False)
    volunteer = db.Column(db.String, nullable=True)
    text = db.Column(db.Text, nullable=False)
