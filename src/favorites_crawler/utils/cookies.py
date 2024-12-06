from __future__ import annotations

import os
from pathlib import Path
from http.cookiejar import MozillaCookieJar

from loguru import logger


def load_cookie(domain: str, home: str | Path) -> dict:
    """Load 'Netscape HTTP Cookie File' as dict"""
    try:
        cookiejar = MozillaCookieJar()
        cookie_file = os.path.join(home, f'{domain}_cookies.txt')
        cookiejar.load(cookie_file)
    except Exception as e:
        logger.error('Failed to load cookie {}, {!r}', cookie_file, e)
        return {}
    return {getattr(c, 'name'): getattr(c, 'value') for c in cookiejar}
