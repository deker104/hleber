from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from models import User


class MakeOrder(FlaskForm):
    user_id = 123
    user = User.query.filter(User.id == user_id)[0]
    username = user.first_name + user.last_name
    phone = StringField("Номер телефона", validators=[DataRequired()], default=user.phone)
    address = StringField("Адрес доставки", validators=[DataRequired()])
    text = TextAreaField("Тескт заказа", validators=[DataRequired()])
    sbm = SubmitField("Заказать")


