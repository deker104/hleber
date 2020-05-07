from hashlib import md5

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_URL
from config import SECRET_KEY
from config import VK_APP_ID
from config import VK_SECRET_KEY
from helpers import is_safe_url

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['USE_SESSION_FOR_NEXT'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Вам необходимо войти для доступа к этой странице.'

if __name__ == '__main__':
    from forms import MakeOrder
    from models import User
    from models import Order


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/order', methods=['POST', 'GET'])
@login_required
def make_order():
    form = MakeOrder()
    if form.validate_on_submit():
        order = Order(
            address=form.address.data,
            phone=form.phone.data,
            client_id=current_user.id,
            text=form.text.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Успешно добавлен новый заказ.')
        return redirect(url_for('myorders'))
    form.phone.data = current_user.phone
    return render_template('make_order.html', form=form)


@app.route('/orders')
@login_required
def orders():
    query = Order.query.all()
    return render_template('orders.html', query=query)


@app.route('/myorders', methods=['POST', 'GET'])
@login_required
def myorders():
    query = Order.query.filter(Order.client == current_user)
    return render_template('myorders.html', query=query)


@app.route('/delete/<id>')
def delete(id):
    db.session.query(Order).filter(Order.id == int(id)).delete()
    db.session.commit()
    next = request.referrer
    if next is None or not is_safe_url(next):
        next = url_for('index')
    flash('Вы удалили запись.')
    return redirect(next)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/vk_auth')
def vk_auth():
    hash_args = request.args.get('hash')
    user_id = request.args.get('uid')
    hash_computed = md5(f'{VK_APP_ID}{user_id}{VK_SECRET_KEY}'.encode()).hexdigest()
    if hash_args == hash_computed:
        user = User.query.get(user_id)
        if user is None:
            user = User(
                id=user_id,
                first_name=request.args.get('first_name'),
                last_name=request.args.get('last_name')
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        next = session.get('next')
        if next is None or not is_safe_url(next):
            next = url_for('index')
        flash('Вы вошли в свой аккаунт.')
        return redirect(next)


@app.route('/test')
def test():
    user = User.query.get(422289484)
    login_user(user)
    flash('Вы вошли в свой аккаунт.')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    next = request.referrer
    if next is None or not is_safe_url(next):
        next = url_for('index')
    flash('Вы вышли из аккаунта.')
    return redirect(next)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

