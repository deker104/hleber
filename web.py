from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_URL, SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/register', methods=['POST', 'GET'])
def reg():
    template = {}
    template["title"] = "Регистрация"
    template["pathcss"] = url_for('static', filename='css/reg.css')
    return render_template('reg.html', **template)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

