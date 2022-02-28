import os

import yaml

config_path = os.path.expanduser('~/.favorites_crawler')
config_file = os.path.join(config_path, 'config.yml')
if not os.path.exists(config_path):
    os.mkdir(config_path)


def load_config():
    """Load config from user home"""
    if not os.path.exists(config_file):
        return {}
    with open(config_file, encoding='utf8') as f:
        return yaml.safe_load(f)


def dump_config(data):
    """Dump config data to user home"""
    with open(config_file, 'w', encoding='utf8') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def overwrite_settings(spider_loader, settings, user_config):
    spider_names = spider_loader.list()
    for name in spider_names:
        cls = spider_loader.load(name)
        spider_config = user_config.get(cls.name, {})
        if spider_config:
            cls.custom_settings.update(spider_config)

        default_files_store = os.path.join(settings.get('FILES_STORE', ''), cls.name)
        cls.custom_settings.setdefault('FILES_STORE', default_files_store)
