import re

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from wtforms.validators import Regexp

__doc__ = """Модуль с формами веб-сайта"""


class PhoneValidator(Regexp):
    """Проверка введёного номера телефона на правильность"""
    regexp = re.compile(r'^\+?[\d\s()-]*$')

    def __init__(self):
        super().__init__(
            self.regexp,
            message='Неправильный формат номера телефона.'
        )


class OrderForm(FlaskForm):
    """Форма создания нового заказа"""
    phone = StringField("Номер телефона", validators=[DataRequired(), PhoneValidator()])
    address = StringField("Адрес доставки", validators=[DataRequired()])
    text = TextAreaField("Текст заказа", validators=[DataRequired()])


class SettingsForm(FlaskForm):
    """Форма изменения настроек"""
    phone = StringField('Номер телефона', validators=[DataRequired(), PhoneValidator()])
    address = StringField('Домашний адрес')

