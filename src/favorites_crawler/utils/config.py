import os
import yaml

DEFAULT_FAVORS_HOME = os.path.expanduser('~/.favorites_crawler')
DEFAULT_CONFIG = {
    'global': {
        'ENABLE_ORGANIZE_BY_ARTIST': True,
        'ENABLE_WRITE_IPTC_KEYWORDS': True,
        'EXIF_TOOL_EXECUTABLE': None,
    },
    'pixiv': {
        'FILES_STORE': 'favorites_crawler_files/pixiv',
        'USER_ID': '',
        'ACCESS_TOKEN': '',
        'REFRESH_TOKEN': '',
    },
    'yandere': {
        'FILES_STORE': 'favorites_crawler_files/yandere',
        'USERNAME': '',
    },
    'twitter': {
        'FILES_STORE': 'favorites_crawler_files/twitter',
        'USER_ID': '',
        'AUTHORIZATION': '',
        'LIKES_ID': '',
        'X_CSRF_TOKEN': '',
    },
    'lemon': {
        'FILES_STORE': 'favorites_crawler_files/lemon',
    },
    'nhentai': {
        'FILES_STORE': 'favorites_crawler_files/nhentai',
    }
}


def load_config(home: str = DEFAULT_FAVORS_HOME) -> dict:
    """Load config from user home"""
    create_favors_home(home)
    config_file = os.path.join(home, 'config.yml')
    if not os.path.exists(config_file):
        dump_config(DEFAULT_CONFIG, home)
        return DEFAULT_CONFIG
    with open(config_file, encoding='utf8') as f:
        return yaml.safe_load(f)


def dump_config(data: dict, home: str = DEFAULT_FAVORS_HOME):
    """Dump config data to user home"""
    create_favors_home(home)
    config_file = os.path.join(home, 'config.yml')
    with open(config_file, 'w', encoding='utf8') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def create_favors_home(path: str):
    """Create favors home if not exists"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def overwrite_spider_settings(spider, default_settings, user_config):
    """
    Overwrite spider settings by user config
    Priority: favors spider config > favors global config > spider custom settings > scrapy settings

    :param spider: Spider class
    :param default_settings: :class:`scrapy.settings.Settings`
    :param user_config: favorites crawler config
    """
    global_config = user_config.get('global')
    if global_config:
        spider.custom_settings.update(global_config)

    spider_config = user_config.get(spider.name)
    if spider_config:
        spider.custom_settings.update(spider_config)

    default_files_store = os.path.join(default_settings.get('FILES_STORE', ''), spider.name)
    spider.custom_settings.setdefault('FILES_STORE', default_files_store)
