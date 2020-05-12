import os
from os.path import join

from dotenv import load_dotenv

__doc__ = """Модуль, собирающий всю конфигурацию проекта"""

BASEDIR = os.path.dirname(os.path.realpath(__file__))

load_dotenv(join(BASEDIR, '.env'))


class Config:
    """Объект, содержащий всю конфигурацию проекта"""
    GEOCODER_KEY = os.getenv('GEOCODER_KEY')
    GEOSEARCH_KEY = os.getenv('GEOSEARCH_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY') or 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + join(BASEDIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VK_APP_ID = os.getenv('VK_APP_ID')
    VK_GROUP_ID = os.getenv('VK_GROUP_ID')
    VK_SECRET_KEY = os.getenv('VK_SECRET_KEY')
    VK_TOKEN = os.getenv('VK_TOKEN')


class TestingConfig(Config):
    """Тестовая конфигурация проекта"""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
