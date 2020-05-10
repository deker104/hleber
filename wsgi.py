from app import create_app

__doc__ = """Скрипт, запускающий Flask-приложение"""

app = create_app()

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
    a
