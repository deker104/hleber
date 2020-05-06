from urllib.parse import urlparse
from urllib.parse import urljoin
from re import compile

from flask import request

VALID_SCHEMES = ['http', 'https']
_substitute_whitespace = compile(r'[\s\x00-\x08\x0B\x0C\x0E-\x19]+').sub
_fix_multiple_slashes = compile(r'(^([^/]+:)?//)/*').sub


def is_safe_url(target):
    # https://github.com/flask-admin/flask-admin/blob/master/flask_admin/helpers.py
    target = target.replace('\\', '/')
    target = _substitute_whitespace('', target)
    target = _fix_multiple_slashes(lambda m: m.group(1), target, 1)
    target_info = urlparse(target)
    target_scheme = target_info.scheme
    if target_scheme and target_scheme not in VALID_SCHEMES:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return ref_url.netloc == test_url.netloc
