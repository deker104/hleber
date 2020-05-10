from flask import current_app

from helpers import build_url

__doc__ = """Модуль с функциями для работы с API Яндекс.Карт"""

geocoder_key = current_app.config.get('GEOCODER_KEY')
geosearch_key = current_app.config.get('GEOSEARCH_KEY')


def geocoder_api(**params):
    """Geocoder API"""
    params.update({
        'apikey': geocoder_key
    })
    return build_url('https://geocode-maps.yandex.ru/1.x/', **params)


def geosearch_api(**params):
    """API Поиска по организациям"""
    params.update({
        'apikey': geosearch_key
    })
    return build_url('https://search-maps.yandex.ru/v1/', **params)


def static_api(**params):
    """Static API"""
    return build_url('https://static-maps.yandex.ru/1.x/', **params)
