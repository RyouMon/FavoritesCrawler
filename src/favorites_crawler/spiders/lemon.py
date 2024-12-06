from scrapy.http import Request
from scrapy.spiders.crawl import Rule, LinkExtractor

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import LemonPicPostItemLoader
from favorites_crawler.constants.endpoints import LEMON_PIC_USER_CENTER_URL, LEMON_PIC_POST_URL_PATTERN
from favorites_crawler.constants.domains import LMMPIC_DOMAIN


class LemonSpider(BaseSpider):
    name = 'lemon'
    allowed_domains = [LMMPIC_DOMAIN]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//ul[@class="my-comment"]'),
            callback='parse', follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="page-links"]', allow='.+html/.+'),
            callback='parse',
        ),
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.ComicPipeline': 0},
    }

    def start_requests(self):
        if hasattr(self, 'id_list') and self.id_list:
            self.logger.debug('GET id_list: %s', self.id_list)
            for i in self.id_list:
                url = LEMON_PIC_POST_URL_PATTERN.format(id=i)
                # parse first page
                yield Request(url=url, cookies=self.cookies, callback=self.parse)
                # apply link extractors on first page
                yield Request(url=url, cookies=self.cookies, dont_filter=True)
        else:
            yield Request(url=LEMON_PIC_USER_CENTER_URL, cookies=self.cookies)

    def parse(self, response, **kwargs):
        loader = LemonPicPostItemLoader(selector=response)
        loader.add_xpath('title', '//h1[@class="entry-title"]/text()')
        loader.add_xpath('file_urls', '//div[@class="single-content"]//img/@src')
        loader.add_xpath('tags', '//a[@rel="tag"]/text()')
        loader.add_value('page', response.url)
        loader.add_value('referer', response.url)
        yield loader.load_item()
