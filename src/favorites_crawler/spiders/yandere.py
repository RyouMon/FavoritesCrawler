from urllib.parse import urlencode

from scrapy import Spider, Request

from favorites_crawler.constants.domains import YANDERE_DOMAIN
from favorites_crawler.itemloaders import YanderePostItemLoader
from favorites_crawler.constants.endpoints import YANDERE_POST_URL
from favorites_crawler.utils.config import load_config


class YandereSpider(Spider):
    """Crawl voted post from yandere"""
    name = 'yandere'
    allowed_domains = (YANDERE_DOMAIN, )
    custom_settings = {
        'ITEM_PIPELINES': {
            'favorites_crawler.pipelines.YandreFilesPipeline': 0,
        },
        'CONCURRENT_REQUESTS': 5,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = load_config().get('yandere', {})
        self.username = config.get('username')
        self.limit = 100
        self.params = {
            'limit': self.limit,
            'page': 1,
            'tags': f'vote:>=1:{self.username}'
        }

    def start_requests(self):
        if self.username:
            yield Request(f'{YANDERE_POST_URL}?{urlencode(self.params)}')

    def parse(self, response, **kwargs):
        posts = response.json()

        if len(posts) == self.limit:
            self.params['page'] += 1
            yield Request(f'{YANDERE_POST_URL}?{urlencode(self.params)}')

        for post in posts:
            loader = YanderePostItemLoader()
            loader.add_value('file_url', post['file_url'])
            yield loader.load_item()
