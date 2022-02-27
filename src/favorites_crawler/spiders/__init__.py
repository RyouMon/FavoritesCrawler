# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from abc import ABCMeta

from scrapy.spiders import CrawlSpider

from favorites_crawler.utils.config import load_config


class BaseSpider(CrawlSpider, metaclass=ABCMeta):

    custom_settings = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        user_config = load_config().get(cls.name, {})
        spider.custom_settings.update(user_config)
