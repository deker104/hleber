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
def order():
    return render_template('make_order.html')


@app.route('/orders')
def orders():
    template = {}
    # oi = ""
    # for i in orders:
    #     oi += f"<p>{i.order}</p><p>{i.text}</p>"
    # template["ordinfo"] = oi
    # TODO
    return render_template('orders.html', **template)


@app.route('/register', methods=['POST', 'GET'])
def reg():
    return render_template('reg.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

