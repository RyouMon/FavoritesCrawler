import os
import yaml

from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

from favorites_crawler.utils.config import (
    create_favors_home, load_config, dump_config, DEFAULT_CONFIG, overwrite_spider_settings)

scrapy_settings = get_project_settings()
spider_loader = SpiderLoader(scrapy_settings)


class TestCreateFavorsHome:
    def test_should_create_path_when_path_exists(self, tmp_path):
        test_path = tmp_path / "existing_dir"
        test_path.mkdir()

        create_favors_home(str(test_path))

        assert test_path.exists()
        assert test_path.is_dir()

    def test_skip_create_path_when_path_not_exists(self, tmp_path):
        test_path = tmp_path / "non_existing_dir"

        create_favors_home(str(test_path))

        assert test_path.exists()
        assert test_path.is_dir()


class TestLoadConfig:
    def test_load_config_when_config_not_exists(self, tmp_path):
        favors_home = str(tmp_path)

        config = load_config(favors_home)

        assert config == DEFAULT_CONFIG
        config_file = os.path.join(favors_home, 'config.yml')
        assert os.path.exists(config_file)

        with open(config_file, encoding='utf8') as f:
            written_config = yaml.safe_load(f)
        assert written_config == DEFAULT_CONFIG

    def test_load_config_when_config_exists(self, tmp_path):
        favors_home = str(tmp_path)
        config_file = os.path.join(favors_home, 'config.yml')
        existing_config = {'global': {'ENABLE_ORGANIZE_BY_ARTIST': False}}

        with open(config_file, 'w', encoding='utf8') as f:
            yaml.safe_dump(existing_config, f)

        config = load_config(favors_home)

        assert config == existing_config


class TestDumpConfig:
    def test_dump_config_to_favors_home(self, tmp_path):
        favors_home = str(tmp_path)
        new_config = {'global': {'ENABLE_ORGANIZE_BY_ARTIST': False}}

        dump_config(new_config, favors_home)

        config_file = os.path.join(favors_home, 'config.yml')
        assert os.path.exists(config_file)

        with open(config_file, encoding='utf8') as f:
            written_config = yaml.safe_load(f)
        assert written_config == new_config


class TestOverwriteSpiderSettings:
    def test_overwrite_spider_settings(self):
        user_config = {
            'global': {
                'ENABLE_ORGANIZE_BY_ARTIST': True,
            },
            'pixiv': {
                'FILES_STORE': '/pixiv',
            }
        }
        spider = spider_loader.load('pixiv')

        overwrite_spider_settings(spider, '~', user_config)

        assert spider.custom_settings['FILES_STORE'] == user_config['pixiv']['FILES_STORE']
        assert spider.custom_settings['ENABLE_ORGANIZE_BY_ARTIST'] == user_config['global']['ENABLE_ORGANIZE_BY_ARTIST']

    def test_spider_config_priority_should_gt_global_config(self):
        user_config = {
            'global': {
                'ENABLE_ORGANIZE_BY_ARTIST': True,
            },
            'yandere': {
                'ENABLE_ORGANIZE_BY_ARTIST': False,
            }
        }
        spider = spider_loader.load('yandere')

        overwrite_spider_settings(spider, '~', user_config)

        assert spider.custom_settings['ENABLE_ORGANIZE_BY_ARTIST'] == user_config['yandere']['ENABLE_ORGANIZE_BY_ARTIST']

    def test_should_set_default_file_store_when_user_doesnt_config_it(self):
        user_config = {}
        spider = spider_loader.load('nhentai')

        overwrite_spider_settings(spider, '~', user_config)

        assert spider.custom_settings['FILES_STORE'] == os.path.expanduser(os.path.join('~', 'nhentai'))

    def test_should_replace_favors_home_in_files_store(self):
        user_config = {'twitter': {'FILES_STORE': os.path.join('$FAVORS_HOME', 'twitter')}}
        spider = spider_loader.load('twitter')

        overwrite_spider_settings(spider, '~', user_config)

        assert spider.custom_settings['FILES_STORE'] == os.path.expanduser(os.path.join('~', 'twitter'))
