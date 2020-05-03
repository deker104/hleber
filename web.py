from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')
