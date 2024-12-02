import shutil
from typing import Optional

import typer
from selenium.common import NoSuchWindowException

from favorites_crawler.utils.auth import CustomGetPixivToken, parse_twitter_likes_url, parser_twitter_likes_features
from favorites_crawler.utils.config import dump_config, load_config
from favorites_crawler.constants.path import DEFAULT_FAVORS_HOME


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
        print("Login successful.")


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
    print("Login successful.")


@app.command('x')
@app.command('twitter')
def login_twitter(
        auth_token: str = typer.Option(
            ..., '-at', '--auth-token',
            help='Authorization Token (Copy from Dev console)'
        ),
        csrf_token: str = typer.Option(
            ..., '-ct', '--csrf-token',
            help='Authorization Token (Copy from Dev console)'
        ),
        likes_url: str = typer.Option(
            ..., '-u', '--likes-url',
            help='Request URL of Likes API (Copy from Dev console)'
        ),
        cookie_file: str = typer.Option(
            ..., '-c', '--cookie-file',
            help='Netscape HTTP Cookie File, you can download it by "Get cookies.txt" browser extension.'
        )
):
    """
    Login to twitter.

    1. Open twitter and login, get to your "Likes" page.\n
    2. Open dev console (F12) and switch to network tab.\n
    3. Enable persistent logging ("Preserve log").\n
    4. Type into the filter field: Likes?\n
    5. Refresh Page.\n
    6. Copy Authorization, X-Csrf-Token and RequestURL from request(Likes?variables...) input on terminal.\n
    7. Use "Get cookies.txt" browser extension download cookie file.
    """
    config = load_config()
    twitter_config = config.setdefault('twitter', {})
    try:
        twitter_config['AUTHORIZATION'] = auth_token
        twitter_config['X_CSRF_TOKEN'] = csrf_token
        twitter_config['LIKES_ID'], twitter_config['USER_ID'] = parse_twitter_likes_url(likes_url)
        twitter_config['FEATURES'] = parser_twitter_likes_features(likes_url)
        shutil.copy(cookie_file, DEFAULT_FAVORS_HOME)
    except Exception as e:
        print(f"Failed to login: {e!r}")
        return
    dump_config(config)
    print("Login successful.")
