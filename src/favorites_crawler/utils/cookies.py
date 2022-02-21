import os
from http.cookiejar import MozillaCookieJar


cookie_home = os.path.expanduser('~/.favorites_crawler')


def load_cookie(domain):
    """Load 'Netscape HTTP Cookie File' as dict"""
    filename = os.path.join(cookie_home, f'{domain}_cookies.txt')
    cookiejar = MozillaCookieJar()
    cookiejar.load(filename)
    return {getattr(c, 'name'): getattr(c, 'value') for c in cookiejar}
