from __future__ import annotations

import os
from pathlib import Path
from copy import deepcopy

import yaml


DEFAULT_CONFIG = {
    'global': {
        'ENABLE_ORGANIZE_BY_ARTIST': True,
        'ENABLE_WRITE_IPTC_KEYWORDS': True,
        'EXIF_TOOL_EXECUTABLE': None,
    },
    'pixiv': {
        'FILES_STORE': os.path.join('$FAVORS_HOME', 'pixiv'),
        'USER_ID': '',
        'ACCESS_TOKEN': '',
        'REFRESH_TOKEN': '',
    },
    'yandere': {
        'FILES_STORE': os.path.join('$FAVORS_HOME', 'yandere'),
        'USERNAME': '',
    },
    'twitter': {
        'FILES_STORE': os.path.join('$FAVORS_HOME', 'twitter'),
        'USER_ID': '',
        'AUTHORIZATION': '',
        'LIKES_ID': '',
        'X_CSRF_TOKEN': '',
    },
    'lemon': {
        'FILES_STORE': os.path.join('$FAVORS_HOME', 'lemon'),
    },
    'nhentai': {
        'USER_AGENT': '',
        'FILES_STORE': os.path.join('$FAVORS_HOME', 'nhentai'),
    }
}


def load_config(home: str | Path) -> dict:
    """Load config from user home"""
    home = os.path.expanduser(home)
    create_favors_home(home)
    config_file = os.path.join(home, 'config.yml')
    if not os.path.exists(config_file):
        dump_config(DEFAULT_CONFIG, home)
        return deepcopy(DEFAULT_CONFIG)
    with open(config_file, encoding='utf8') as f:
        return yaml.safe_load(f)


def dump_config(data: dict, home: str | Path):
    """Dump config data to user home"""
    home = os.path.expanduser(home)
    create_favors_home(home)
    config_file = os.path.join(home, 'config.yml')
    with open(config_file, 'w', encoding='utf8') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def create_favors_home(path: str | Path):
    """Create favors home if not exists"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def overwrite_spider_settings(spider, home, user_config):
    """
    Overwrite spider settings by user config
    Priority: favors spider config > favors global config > spider custom settings > scrapy settings

    :param spider: Spider class
    :param home: favors home
    :param user_config: favorites crawler config
    """
    global_config = user_config.get('global')
    if global_config:
        spider.custom_settings.update(global_config)

    spider_config = user_config.get(spider.name, {})
    if spider_config:
        spider.custom_settings.update(spider_config)

    home = os.path.expanduser(home)
    files_store = spider_config.get('FILES_STORE')
    if files_store:
        spider.custom_settings['FILES_STORE'] = files_store.replace('$FAVORS_HOME', home)
    else:
        spider.custom_settings['FILES_STORE'] = os.path.join(home, spider.name)
