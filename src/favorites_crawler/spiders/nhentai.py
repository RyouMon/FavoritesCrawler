from scrapy.spiders.crawl import Rule, LinkExtractor
from scrapy.http import Request

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import NHentaiGalleryItemLoader
from favorites_crawler.constants.endpoints import NHENTAI_USER_FAVORITES_URL
from favorites_crawler.constants.domains import NHENTAI_DOMAIN
from favorites_crawler.utils.cookies import load_cookie


class NHentaiSpider(BaseSpider):
    name = 'nhentai'
    allowed_domains = (NHENTAI_DOMAIN, )
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="container"]'), callback='parse'),
    )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookies = load_cookie(NHENTAI_DOMAIN)

    def start_requests(self):
        yield Request(NHENTAI_USER_FAVORITES_URL, cookies=self.cookies)

    def parse(self, response, **kwargs):
        loader = NHentaiGalleryItemLoader(selector=response)
        loader.add_value('id', response.url)
        loader.add_value('referer', response.url)
        loader.add_xpath('title', '//h1[@class="title"]/span/text()')
        loader.add_xpath('tags', '//section[@id="tags"]/div[3]//span[@class="name"]/text()')
        loader.add_xpath('image_urls', '//div[@id="thumbnail-container"]//img/@data-src')
        loader.add_xpath('characters', '//section[@id="tags"]/div[2]//span[@class="name"]/text()')
        yield loader.load_item()
