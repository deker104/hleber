from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

__doc__ = """Модуль с формами веб-сайта"""


class OrderCreate(FlaskForm):
    """Форма создания нового заказа"""
    phone = StringField("Номер телефона", validators=[DataRequired()])
    address = StringField("Адрес доставки", validators=[DataRequired()])
    text = TextAreaField("Текст заказа", validators=[DataRequired()])

