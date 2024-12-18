import re
from pathlib import Path

from scrapy.spiders.crawl import Rule, LinkExtractor, Link
from scrapy.http import Request

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import NHentaiGalleryItemLoader
from favorites_crawler.constants.endpoints import NHENTAI_USER_FAVORITES_URL
from favorites_crawler.constants.domains import NHENTAI_DOMAIN
from favorites_crawler.utils.files import list_comics


class NHentaiSpider(BaseSpider):
    name = 'nhentai'
    allowed_domains = (NHENTAI_DOMAIN, )
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//section[@class="pagination"]'),
            process_request='add_cookies',
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="container"]'),
            callback='parse',
            process_links='filter_exists_comics',
            process_request='add_cookies',
        ),
    )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.ComicPipeline': 0},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comics = {}

    def start_requests(self):
        self.comics = list_comics(Path(self.settings.get('FILES_STORE')))
        yield Request(NHENTAI_USER_FAVORITES_URL, cookies=self.cookies)

    def parse(self, response, **kwargs):
        loader = NHentaiGalleryItemLoader(selector=response)

        loader.add_value('id', response.url)
        loader.add_value('referer', response.url)
        loader.add_xpath('file_urls', '//div[@id="thumbnail-container"]//img/@data-src')
        loader.add_xpath('sort_title', '//h1[@class="title"]/span/text()')
        loader.add_xpath('parodies', '//h2[@class="title"]/span[@class="after"]/text()')
        loader.add_xpath('parodies', '//section[@id="tags"]/div[1]//span[@class="name"]/text()')
        loader.add_xpath('characters', '//section[@id="tags"]/div[2]//span[@class="name"]/text()')

        loader.add_xpath('title', '//h2[@class="title"]/span/text()')
        loader.add_xpath('title', '//h1[@class="title"]/span/text()')
        loader.add_value('series', loader.get_output_value('title'))
        loader.add_value('volume', loader.get_output_value('title'))
        loader.add_xpath('language', '//section[@id="tags"]/div[6]//span[@class="name"]/text()')
        loader.add_xpath('genre', '//section[@id="tags"]/div[7]//span[@class="name"]/text()')
        loader.add_xpath('credits', '//section[@id="tags"]/div[4]//span[@class="name"]/text()')  # Artists
        loader.add_xpath('credits', '//section[@id="tags"]/div[5]//span[@class="name"]/text()')  # Groups
        loader.add_xpath('tags', '//section[@id="tags"]/div[3]//span[@class="name"]/text()')
        loader.add_value('tags', loader.get_output_value('characters'))
        loader.add_value('tags', loader.get_output_value('parodies'))
        loader.add_xpath('publicationYear', '//section[@id="tags"]/div[9]//time/@datetime')
        loader.add_xpath('publicationMonth', '//section[@id="tags"]/div[9]//time/@datetime')
        loader.add_value('publisher', 'nhentai')

        yield loader.load_item()

    def filter_exists_comics(self, links: list[Link]):
        def comic_not_exists(link):
            comic_id = re.match(r'^.*?(\d+).*?$', link.url)
            if not comic_id:
                return True
            if comic_id.group(1) in self.comics:
                self.logger.info('Comic already downloaded, filter URL: %s', link)
                self.crawler.stats.inc_value('already_downloaded/filtered')
                return False
            return True

        return list(filter(comic_not_exists, links))

    def add_cookies(self, request, _):
        request.cookies = self.cookies
        return request
