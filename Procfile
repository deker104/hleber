release: flask db upgrade
web: gunicorn app.wsgi:app
worker: python vk/bot.py