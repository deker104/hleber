import os
from os.path import join

from dotenv import load_dotenv

BASEDIR = os.path.dirname(os.path.realpath(__file__))

load_dotenv(join(BASEDIR, '.env'))

VK_TOKEN = os.getenv('VK_TOKEN')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')
DATABASE_URL = os.getenv('DATABASE_URL') or 'sqlite:///' + join(BASEDIR, 'db.sqlite3')
SECRET_KEY = os.getenv('SECRET_KEY') or 'test-secret-key'
