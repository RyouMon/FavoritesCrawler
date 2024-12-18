# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from abc import ABCMeta

from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider

from favorites_crawler.utils.common import get_favors_home
from favorites_crawler.utils.config import load_config, dump_config


class BaseSpider(CrawlSpider, metaclass=ABCMeta):
    custom_settings = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_bookmark_id = self.custom_settings.get('LAST_BOOKMARK_ID')
        self.last_bookmark_id_updated = False

    def close_spider_when_bookmark_not_updated(self, response, **kwargs):
        """Close spider when bookmark not updated"""
        last_bookmark_id = self.get_last_bookmark_id(response, **kwargs)
        self._close_spider_when_bookmark_not_updated(last_bookmark_id)
        self.update_last_bookmark_id(last_bookmark_id)

    def get_last_bookmark_id(self, response, **kwargs):
        """Get last bookmark id from start_url response"""
        raise NotImplementedError()

    def _close_spider_when_bookmark_not_updated(self, bookmark_id):
        """Close spider when current bookmark id equals to last bookmark id."""
        if self.last_bookmark_id and (self.last_bookmark_id == bookmark_id):
            self.logger.info('Bookmark not updated, closing spider.')
            raise CloseSpider('fastly-finished')

    def update_last_bookmark_id(self, bookmark_id):
        """Update last bookmark id"""
        if not bookmark_id or self.last_bookmark_id_updated:
            return
        self.last_bookmark_id = bookmark_id
        self.last_bookmark_id_updated = True
        favors_home = get_favors_home()
        config = load_config(favors_home)
        spider_config = config.setdefault(self.name, {})
        spider_config['LAST_BOOKMARK_ID'] = bookmark_id
        dump_config(config, favors_home)
        self.logger.info('Updated LAST_BOOKMARK_ID: %s', bookmark_id)
