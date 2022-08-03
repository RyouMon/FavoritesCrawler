from urllib.parse import urlencode

from scrapy import Request
from scrapy.exceptions import CloseSpider

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.constants.domains import YANDERE_DOMAIN
from favorites_crawler.itemloaders import YanderePostItemLoader
from favorites_crawler.constants.endpoints import YANDERE_POST_URL


class YandereSpider(BaseSpider):
    """Crawl voted post from yandere"""
    name = 'yandere'
    allowed_domains = (YANDERE_DOMAIN, )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = 100
        self.params = {'page': 1, 'limit': self.limit}

    def start_requests(self):
        username = self.custom_settings.get('USERNAME')
        if not username:
            raise CloseSpider('Did you run "favors login yandere"?')

        self.params['tags'] = f'vote:>=1:{username}'
        yield Request(f'{YANDERE_POST_URL}?{urlencode(self.params)}')

    def parse_start_url(self, response, **kwargs):
        for request_or_item in self.parse(response, **kwargs):
            yield request_or_item

    def parse(self, response, **kwargs):
        """Spider Contracts:
        @url https://yande.re/post.json?limit=100&page=1
        @returns item 100
        @returns requests 1
        @scrapes file_urls
        """
        posts = response.json()

        if len(posts) == self.limit:
            self.params['page'] += 1
            yield Request(f'{YANDERE_POST_URL}?{urlencode(self.params)}')

        for post in posts:
            loader = YanderePostItemLoader()
            loader.add_value('file_urls', post['file_url'])
            yield loader.load_item()
