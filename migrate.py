from web import User
from web import db

db.drop_all()
db.create_all()

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
