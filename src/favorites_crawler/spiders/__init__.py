# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from abc import ABCMeta

from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider, metaclass=ABCMeta):

    custom_settings = {}
