from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class MakeOrder(FlaskForm):
    phone = StringField("Номер телефона", validators=[DataRequired()])
    address = StringField("Адрес доставки", validators=[DataRequired()])
    text = TextAreaField("Текст заказа", validators=[DataRequired()])

