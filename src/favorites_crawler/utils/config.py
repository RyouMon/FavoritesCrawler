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
        yaml.safe_dump(data, f)
