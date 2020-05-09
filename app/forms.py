from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.validators import Regexp

from helpers import check_phone

__doc__ = """Модуль с формами веб-сайта"""

phone_validator = lambda: Regexp(check_phone, message="Неправильно введён номер телефона.")


class OrderCreateForm(FlaskForm):
    """Форма создания нового заказа"""
    phone = StringField("Номер телефона", validators=[DataRequired(), phone_validator()])
    address = StringField("Адрес доставки", validators=[DataRequired()])
    text = TextAreaField("Текст заказа", validators=[DataRequired()])


class SettingsForm(FlaskForm):
    """Форма изменения настроек"""
    phone = StringField('Номер телефона', validators=[phone_validator()])
    address = StringField('Домашний адрес')

