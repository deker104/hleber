import os
from os.path import join

from dotenv import load_dotenv

BASEDIR = os.path.dirname(os.path.realpath(__file__))

load_dotenv(join(BASEDIR, '.env'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + join(BASEDIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True


VK_TOKEN = os.getenv('VK_TOKEN')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')
VK_SECRET_KEY = os.getenv('VK_SECRET_KEY')
VK_APP_ID = os.getenv('VK_APP_ID') or '7451096'
