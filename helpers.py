from re import compile
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.parse import urlparse

from flask import request

__doc__ = """Модуль вспомогательных функций"""

VALID_SCHEMES = ['http', 'https']
_substitute_whitespace = compile(r'[\s\x00-\x08\x0B\x0C\x0E-\x19]+').sub
_fix_multiple_slashes = compile(r'(^([^/]+:)?//)/*').sub


def is_safe_url(target):
    """Функция, проверяющая URL в target на безопасность.
    Взято здесь:
    https://github.com/flask-admin/flask-admin/blob/master/flask_admin/helpers.py
    """
    # избавиться от url по типу "\\www.google.com"
    # некоторые браузеры сами меняют \\ на // (например: Chrome)
    # взято здесь: https://stackoverflow.com/questions/10438008
    target = target.replace('\\', '/')

    # обработать случаи по типу "j a v a s c r i p t:"
    target = _substitute_whitespace('', target)

    # Chrome и FireFox сами "исправляют" лишние сплеши после протокола
    target = _fix_multiple_slashes(lambda m: m.group(1), target, 1)

    # избавиться от url с "javascript:"
    target_info = urlparse(target)
    target_scheme = target_info.scheme
    if target_scheme and target_scheme not in VALID_SCHEMES:
        return False

    # проверить хост
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return ref_url.netloc == test_url.netloc


def build_url(url_base, **params):
    """Функция для удобного построения URL"""
    return url_base + urlencode(params)
