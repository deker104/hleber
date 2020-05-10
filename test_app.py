from app import create_app
from app import db
from app.models import User
from config import TestingConfig

__doc__ = """Скрипт, загружающий в БД тестовые данные"""


def test_db():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        load_data()
        user = User.query.get(422289484)
        assert user.first_name == 'Макс'
        assert user.phone is None


def load_data():
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


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        load_data()
