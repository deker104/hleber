from flask import Blueprint
from flask import render_template

__doc__ = """Модуль главной страницы"""

blueprint = Blueprint('main', __name__, template_folder='templates')


@blueprint.route('/')
@blueprint.route('/index')
def index():
    """Главная страница"""
    return render_template('index.html')
