import os
from http.cookiejar import MozillaCookieJar


cookie_home = os.path.expanduser('~/.favorites_crawler')


def load_cookie(domain):
    """Load 'Netscape HTTP Cookie File' as dict"""
    filename = f'{domain}_cookies.txt'
    try:
        cookiejar = MozillaCookieJar()
        cookiejar.load(os.path.join(cookie_home, filename))
    except FileNotFoundError as error:
        raise FileNotFoundError(f'{filename} not exists.') from error
    else:
        return {getattr(c, 'name'): getattr(c, 'value') for c in cookiejar}
