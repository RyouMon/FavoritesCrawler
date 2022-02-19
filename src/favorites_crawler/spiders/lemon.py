from scrapy.http import FormRequest, Request
from scrapy.spiders.crawl import CrawlSpider, Rule, LinkExtractor
from scrapy.exceptions import CloseSpider

from favorites_crawler.itemloaders import LemonPicPostItemLoader
from favorites_crawler.constants.endpoints import LEMON_PIC_LOGIN_URL, LEMON_PIC_USER_FAVORITES_URL
from favorites_crawler.utils.config import load_config


class LemonSpider(CrawlSpider):
    name = 'lemon'
    allowed_domains = ['lmmpic.com']
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="my-favorite"]', allow='.+html', deny='#'),
            callback='parse_item', follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="page-links"]', allow='.+html/.+'),
            callback='parse_item',
        ),
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.CollectionFilePipeline': 0},
    }

    def __init__(self, **kwargs):
        super(LemonSpider, self).__init__(**kwargs)
        config = load_config().get('lmmpic', {})
        self.username = config.get('username', '')
        self.password = config.get('password', '')

    def start_requests(self):
        yield Request(url=LEMON_PIC_LOGIN_URL, callback=self.login)

    def login(self, response):
        yield FormRequest.from_response(
            formdata={'log': self.username, 'pwd': self.password},
            response=response, callback=self.after_login,
        )

    def after_login(self, response):
        if response.url != LEMON_PIC_USER_FAVORITES_URL:
            self.logger.warn('Your username or password may not be valid.')
            raise CloseSpider('not login')

        for request_or_item in self._requests_to_follow(response):
            yield request_or_item

    def parse_item(self, response, **kwargs):
        loader = LemonPicPostItemLoader(selector=response)
        loader.add_xpath('title', '//h1[@class="entry-title"]/text()')
        loader.add_xpath('image_urls', '//div[@class="single-content"]//img/@src')
        loader.add_xpath('tags', '//a[@rel="tag"]/text()')
        loader.add_value('referer', response.url)
        yield loader.load_item()
