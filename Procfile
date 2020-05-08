release: flask db upgrade
web: gunicorn wsgi:app
worker: python vk.py