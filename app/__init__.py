from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
from maps import Maps

__doc__ = """Модуль веб-сайта"""

# Подключение всех дополненией
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Вам необходимо войти для доступа к этой странице.'
maps = Maps()


def create_app(config=Config):
    """Фабрика приложений - удобный способ создания новых экземпляров приложения"""
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    maps.init_app(app)

    from app.orders import blueprint as orders_bp
    app.register_blueprint(orders_bp)

    from app.auth import blueprint as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import blueprint as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models
