import re
from urllib.parse import unquote
from webbrowser import open as open_url

from gppt import GetPixivToken
from gppt.consts import REDIRECT_URI
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from favorites_crawler.constants.endpoints import TWITTER_PROFILE_LIKES_URL
from favorites_crawler.utils.config import dump_config, load_config
from favorites_crawler.settings import PIXIV_LOGIN_TIMEOUT


class CustomGetPixivToken(GetPixivToken):
    def _GetPixivToken__wait_for_redirect(self) -> None:
        # Overwrite timeout value
        try:
            WebDriverWait(self.driver, PIXIV_LOGIN_TIMEOUT).until(EC.url_matches(f"^{REDIRECT_URI}"))
        except TimeoutException as err:
            self.driver.close()
            msg = "Failed to login. Please check your information or proxy. (Maybe restricted by pixiv?)"
            raise ValueError(msg) from err


def login_pixiv():
    config = load_config()
    token_getter = CustomGetPixivToken()
    login_info = token_getter.login()

    pixiv_config = config.setdefault('pixiv', {})
    try:
        pixiv_config['USER_ID'] = login_info['user']['id']
        pixiv_config['ACCESS_TOKEN'] = login_info['access_token']
        pixiv_config['REFRESH_TOKEN'] = login_info['refresh_token']
    except KeyError as e:
        print(f'Failed to get pixiv config from: {login_info}, {e!r}')
    else:
        print("Login successful.")
        dump_config(config)
    return pixiv_config


def refresh_pixiv():
    config = load_config()
    pixiv_config = config.get('pixiv', {})
    refresh_token = pixiv_config.get('REFRESH_TOKEN')
    if not refresh_token:
        raise ValueError('Cannot find refresh_token in config file, did you run `favors login pixiv`?')
    token_getter = CustomGetPixivToken()
    login_info = token_getter.refresh(refresh_token)
    access_token = login_info['access_token']
    pixiv_config['ACCESS_TOKEN'] = access_token
    dump_config(config)
    return access_token


def auth_yandere():
    config = load_config()
    try:
        username = input("username: ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    yandere_config = config.setdefault('yandere', {})
    yandere_config['USERNAME'] = username
    dump_config(config)
    return yandere_config


def auth_twitter():
    username = input('username: ').strip()
    open_url(TWITTER_PROFILE_LIKES_URL.format(username=username))

    config = load_config()
    twitter_config = config.setdefault('twitter', {})
    twitter_config['AUTHORIZATION'] = input('Authorization: ')
    twitter_config['X_CSRF_TOKEN'] = input('X-Csrf-Token: ')
    twitter_config['LIKES_ID'], twitter_config['USER_ID'] = parse_twitter_likes_url(input('Request URL: '))
    dump_config(config)
    return twitter_config


def parse_twitter_likes_url(url):
    url = unquote(url).replace(' ', '')
    match = re.match(r'^.+?graphql/(.+?)/.+?userId":"(.+?)".+$', url)
    return match.groups()
