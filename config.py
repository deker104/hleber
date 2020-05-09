import os
from os.path import join

from dotenv import load_dotenv

__doc__ = """Модуль, собирающий всю конфигурацию проекта"""

BASEDIR = os.path.dirname(os.path.realpath(__file__))

load_dotenv(join(BASEDIR, '.env'))


class Config:
    """Объект, содержащий всю конфигурацию проекта"""
    SECRET_KEY = os.getenv('SECRET_KEY') or 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + join(BASEDIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True
    VK_APP_ID = os.getenv('VK_APP_ID') or '7451096'
    VK_GROUP_ID = os.getenv('VK_GROUP_ID')
    VK_SECRET_KEY = os.getenv('VK_SECRET_KEY')
    VK_TOKEN = os.getenv('VK_TOKEN')
