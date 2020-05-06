from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

from models import *


class MakeOrder(FlaskForm):
    user_id = 123
    # user = User.query.filter(User.id == user_id)[0]
    username = "Макс Касик"
    phone = StringField("Номер телефона", validators=[DataRequired()], default='88005553535')
    address = StringField("Адрес доставки", validators=[DataRequired()])
    text = TextAreaField("Тескт заказа", validators=[DataRequired()])
