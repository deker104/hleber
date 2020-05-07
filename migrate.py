from web import db
from web import User

db.drop_all()
db.create_all()

user = User(
    id=422289484,
    first_name='Макс',
    last_name='Зарянов'
)
db.session.add(user)
db.session.commit()
