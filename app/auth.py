from hashlib import md5

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import current_user
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user

from app import db
from app.forms import SettingsForm
from helpers import is_safe_url
from app.models import User

__doc__ = """Все веб-страницы и функции, связанные с авторизацией пользователей"""

blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/login')
def login():
    """Страница входа через ВКонтакте"""
    return render_template('login.html')


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm(obj=current_user)
    if form.validate_on_submit():
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        db.session.add(current_user)
        db.session.commit()
        flash('Настройки успешно изменены.')
        return redirect(url_for('.settings'))
    return render_template('users_settings.html', form=form)


@blueprint.route('/auth')
def auth():
    """Обработка авторизации ВКонтакте"""
    hash_args = request.args.get('hash')
    user_id = request.args.get('uid')
    app_id = current_app.config.get('VK_APP_ID')
    secret_key = current_app.config.get('VK_SECRET_KEY')
    hash_computed = md5(f'{app_id}{user_id}{secret_key}'.encode()).hexdigest()
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
            flash('Вы успешно зарегестрировались. '
                  'Сейчас вы можете дополнительно настроить свой профиль.')
            return redirect(url_for('.settings'))
        login_user(user)
        next = session.get('next')
        if next is None or not is_safe_url(next):
            next = url_for('main.index')
        flash('Вы вошли в свой аккаунт.')
        session['next'] = ''
        return redirect(next)


@blueprint.route('/test/<int:id>')
def test(id):
    """Тестовый вход по id пользователя"""
    if not current_user.is_authenticated and current_app.debug:
        user = User.query.get(id)
        if user is not None:
            login_user(user)
            flash('Вы вошли в свой аккаунт.')
        else:
            flash('Не удалось войти!')
    return redirect(url_for('main.index'))


@blueprint.route('/logout')
def logout():
    """Выход из аккаунта"""
    if current_user.is_authenticated:
        logout_user()
        flash('Вы вышли из аккаунта.')
    next = request.referrer
    if next is None or not is_safe_url(next):
        next = url_for('main.index')
    return redirect(next)
