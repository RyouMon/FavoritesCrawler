from gppt import GetPixivToken
from gppt.consts import REDIRECT_URI
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
