import os
from http.cookiejar import MozillaCookieJar


cookie_home = os.path.expanduser('~/.favorites_crawler')


def load_cookie(domain):
    """Load 'Netscape HTTP Cookie File' as dict"""
    cookiejar = MozillaCookieJar()
    cookiejar.load(os.path.join(cookie_home, f'{domain}_cookies.txt'))
    return {getattr(c, 'name'): getattr(c, 'value') for c in cookiejar}
