from scrapy.http import Request
from scrapy.spiders.crawl import Rule, LinkExtractor

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import LemonPicPostItemLoader
from favorites_crawler.constants.endpoints import LEMON_PIC_USER_FAVORITES_URL
from favorites_crawler.constants.domains import LMMPIC_DOMAIN
from favorites_crawler.utils.cookies import load_cookie


class LemonSpider(BaseSpider):
    name = 'lemon'
    allowed_domains = [LMMPIC_DOMAIN]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="my-favorite"]', allow='.+html', deny='#'),
            callback='parse', follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="page-links"]', allow='.+html/.+'),
            callback='parse',
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookies = load_cookie(LMMPIC_DOMAIN)

    def start_requests(self):
        yield Request(url=LEMON_PIC_USER_FAVORITES_URL, cookies=self.cookies)

    def parse(self, response, **kwargs):
        loader = LemonPicPostItemLoader(selector=response)
        loader.add_xpath('title', '//h1[@class="entry-title"]/text()')
        loader.add_xpath('file_urls', '//div[@class="single-content"]//img/@src')
        loader.add_xpath('tags', '//a[@rel="tag"]/text()')
        loader.add_value('referer', response.url)
        yield loader.load_item()
