from hashlib import md5

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

from app import db
from app.helpers import is_safe_url
from app.models import User
from config import VK_APP_ID
from config import VK_SECRET_KEY

blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/login')
def login():
    return render_template('login.html')


@blueprint.route('/auth')
def auth():
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
            next = url_for('main.index')
        flash('Вы вошли в свой аккаунт.')
        session['next'] = ''
        return redirect(next)


@blueprint.route('/test/<int:id>')
def test(id):
    if not current_user.is_authenticated:
        user = User.query.get(id)
        if user is not None:
            login_user(user)
            flash('Вы вошли в свой аккаунт.')
        else:
            flash('Не удалось войти!')
    return redirect(url_for('main.index'))


@blueprint.route('/logout')
def logout():
    logout_user()
    next = request.referrer
    if next is None or not is_safe_url(next):
        next = url_for('main.index')
    flash('Вы вышли из аккаунта.')
    return redirect(next)
