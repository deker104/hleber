from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/order')
def make_order():
    return render_template('make_order.html')


@app.route('/orders')
def orders():
    query = Order.query.all()
    return render_template('orders.html', query=query)


@app.route('/register', methods=['POST', 'GET'])
def reg():
    return render_template('reg.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

