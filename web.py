from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import db_session
from models import *

from config import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
db_session.global_init("orders.sqlite")
session = db_session.create_session()
orders = session.query(Order).all()
users = session.query(User).all()
print(orders)



@app.route('/')
@app.route('/index')
def index():
    template = {}
    template["title"] = "Deliver"
    template["pathcss"] = url_for('static', filename='css/style.css')
    return render_template('index.html', **template)


@app.route('/order')
def order():
    template = {}
    template["title"] = "Заказ товаров"
    template["pathcss"] = url_for('static', filename='css/ord.css')
    return render_template('makeorder.html', **template)


@app.route('/orders')
def orders():
    template = {}
    oi = ""
    for i in orders:
        oi += f"<p>{i.order}</p><p>{i.text}</p>"
    template["ordinfo"] = oi

    return render_template('orders.html', **template)


@app.route('/register', methods=['POST', 'GET'])
def reg():
    template = {}
    template["title"] = "Регистрация"
    template["pathcss"] = url_for('static', filename='css/reg.css')
    return render_template('reg.html', **template)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

