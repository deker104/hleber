from web import db
from web import User

db.drop_all()
db.create_all()

user = User(
    id=463526827,
    first_name='Даниил',
    last_name='Шиндов'
)
db.session.add(user)
db.session.commit()
