import requests

from helpers import build_url

__doc__ = """Модуль с функциями для работы с API Яндекс.Карт"""


class Maps:
    """Flask-дополнение для работы с Яндекс.Картами"""
    def __init__(self, app=None):
        self.geocoder_key = None
        self.geosearch_key = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Привязка дополнения к конкретному экземпляру приложения"""
        self.geocoder_key = app.config.get('GEOCODER_KEY')
        self.geosearch_key = app.config.get('GEOSEARCH_KEY')

    def geocoder_api(self, **params):
        """Geocoder API"""
        params.update({
            'apikey': self.geocoder_key,
            'format': 'json'
        })
        return requests.get('https://geocode-maps.yandex.ru/1.x/', params).json()

    def geosearch_api(self, **params):
        """API Поиска по организациям"""
        params.update({
            'apikey': self.geosearch_key,
            "lang": "ru_RU",
            'format': 'json'
        })
        return requests.get('https://search-maps.yandex.ru/v1/', params).json()

    def static_api(self, l, **params):
        """Static API"""
        params.update({
            'l': l
        })
        return build_url('https://static-maps.yandex.ru/1.x/', **params)
