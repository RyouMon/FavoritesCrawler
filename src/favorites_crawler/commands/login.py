import re
from typing import Optional
from urllib.parse import unquote
from webbrowser import open as open_url

import typer
from selenium.common import NoSuchWindowException

from favorites_crawler.constants.endpoints import TWITTER_PROFILE_LIKES_URL
from favorites_crawler.utils.auth import CustomGetPixivToken
from favorites_crawler.utils.config import dump_config, load_config


app = typer.Typer(help='Prepare auth information for crawling.', no_args_is_help=True)


@app.command('pixiv')
def login_pixiv(
        username: Optional[str] = typer.Option(
            None, '-u', '--username',
            help='Your pixiv email or user id.'
        ),
        password: Optional[str] = typer.Option(
            None, '-p', '--password',
            help='Your pixiv password.'
        )
):
    """
    Login to pixiv.

    When you provide your username and password, the browser will automatically enter them and login.

    Note: pixiv may ask you to provide a verification code via email when you login,
    and you will need to enter the verification code manually.

    If you do not provide your username and password, you will login manually on the web page
    """
    config = load_config()
    token_getter = CustomGetPixivToken()
    try:
        login_info = token_getter.login(username=username, password=password)
    except NoSuchWindowException:
        print('Failed to login.')
        return

    pixiv_config = config.setdefault('pixiv', {})
    try:
        pixiv_config['USER_ID'] = login_info['user']['id']
        pixiv_config['ACCESS_TOKEN'] = login_info['access_token']
        pixiv_config['REFRESH_TOKEN'] = login_info['refresh_token']
    except KeyError as e:
        print(f'Failed to login. {e!r}')
    else:
        dump_config(config)


@app.command('yandere')
def login_yandere(
        username: str = typer.Option(
            ..., '-u', '--username',
            help="Your yandere username."
        )
):
    """
    Login to yandere.
    """
    config = load_config()
    yandere_config = config.setdefault('yandere', {})
    yandere_config['USERNAME'] = username
    dump_config(config)


@app.command('x')
@app.command('twitter')
def login_twitter(
        username: str = typer.Option(
            ..., '-u', '--username',
            help="Your twitter username."
        )
):
    """
    Login to twitter.

    1. After execute this command, likes page will open in browser.\n
    2. Open dev console (F12) and switch to network tab.\n
    3. Enable persistent logging ("Preserve log").\n
    4. Type into the filter field: Likes?\n
    5. Refresh Page.\n
    6. Copy Authorization, X-Csrf-Token and RequestURL from request(Likes?variables...) input on terminal.\n
    7. Use "Get cookies.txt" browser extension download cookie file.\n
    8. Copy cookie file to {user_home}/.favorites_crawler.
    """
    open_url(TWITTER_PROFILE_LIKES_URL.format(username=username))
    config = load_config()
    twitter_config = config.setdefault('twitter', {})
    try:
        twitter_config['AUTHORIZATION'] = input('Authorization: ')
        twitter_config['X_CSRF_TOKEN'] = input('X-Csrf-Token: ')
        twitter_config['LIKES_ID'], twitter_config['USER_ID'] = parse_twitter_likes_url(input('Request URL: '))
    except KeyboardInterrupt:
        "Failed to login."
        return
    dump_config(config)


def parse_twitter_likes_url(url):
    """Parse USER_ID and LIKES_ID from URL"""
    url = unquote(url).replace(' ', '')
    match = re.match(r'^.+?graphql/(.+?)/.+?userId":"(.+?)".+$', url)
    return match.groups()
