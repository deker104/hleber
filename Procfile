release: FLASK_APP=web.py flask db upgrade
web: gunicorn web:app
worker: python vk.py