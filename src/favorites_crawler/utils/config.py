import os

import yaml

config_path = os.path.expanduser('~/.favorites_crawler')
if not os.path.exists(config_path):
    os.mkdir(config_path)


def load_config(config_name):
    """Load config from user home"""
    config_file = os.path.join(config_path, config_name)
    if not os.path.exists(config_file):
        return {}
    with open(config_file, encoding='utf8') as f:
        return yaml.safe_load(f)


def dump_config(config_name, data):
    """Dump config data to user home"""
    config_file = os.path.join(config_path, config_name)
    with open(config_file, 'w', encoding='utf8') as f:
        yaml.safe_dump(data, f)
