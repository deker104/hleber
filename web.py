from hashlib import md5

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import LoginManager
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
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

from models import User
from orders import blueprint as orders_bp


app.register_blueprint(orders_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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


@app.route('/test/<int:id>')
def test(id):
    if not current_user.is_authenticated:
        user = User.query.get(id)
        if user is not None:
            login_user(user)
            flash('Вы вошли в свой аккаунт.')
        else:
            flash('Не удалось войти!')
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

