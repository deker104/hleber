from app import create_app
from app import db
from app.models import User

__doc__ = """Скрипт, загружающий в БД тестовые данные"""

app = create_app()

with app.app_context():
    user = User(
        id=422289484,
        first_name='Макс',
        last_name='Зарянов'
    )
    db.session.add(user)
    user = User(
        id=463526827,
        first_name='Даниил',
        last_name='Шиндов'
    )
    db.session.add(user)
    db.session.commit()
