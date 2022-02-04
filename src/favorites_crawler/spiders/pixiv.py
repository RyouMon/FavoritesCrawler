import json
from urllib.parse import urlencode

from scrapy import Spider, Request

from favorites_crawler.itemloaders import PixivIllustItemLoader
from favorites_crawler.constants.domains import PIXIV_DOMAIN
from favorites_crawler.constants.endpoints import PIXIV_USER_BOOKMARKS_ENDPOINT
from favorites_crawler.constants.headers import PIXIV_REQUEST_HEADERS, PIXIV_IOS_USER_AGENT
from favorites_crawler.utils.config import load_config


class PixivSpider(Spider):
    """Crawl user bookmarks in pixiv"""
    name = 'pixiv'
    allowed_domains = (PIXIV_DOMAIN, )
    custom_settings = {
        'USER_AGENT': PIXIV_IOS_USER_AGENT,
        'DEFAULT_REQUEST_HEADERS': PIXIV_REQUEST_HEADERS,
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.PixivFilesPipeline': 0},
        # Add PixivAuthorizationMiddleware after DefaultHeadersMiddleware
        'DOWNLOADER_MIDDLEWARES': {'favorites_crawler.middlewares.PixivAuthorizationMiddleware': 450},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = load_config('pixiv.yml').get('user_id')

    def start_requests(self):
        if self.user_id:
            params = {
                'user_id': self.user_id,
                'restrict': 'public',
                'filter': 'for_ios',
            }
            yield Request(f'{PIXIV_USER_BOOKMARKS_ENDPOINT}?{urlencode(params)}')

    def parse(self, response, **kwargs):
        result = json.loads(response.text)
        next_link = result.get('next_url')
        if next_link:
            yield response.follow(next_link)

        illust_list = result.get('illusts', ())
        for illust in illust_list:
            loader = PixivIllustItemLoader()
            loader.add_value('id', illust.get('id'))
            loader.add_value('title', illust.get('title'))
            loader.add_value('tags', illust.get('tags'))
            loader.add_value('original_image_urls', illust.get('meta_single_page', {}).get('original_image_url', ()))
            loader.add_value('original_image_urls', [
                d['image_urls']['original'] for d in illust.get('meta_pages', ())
                if d.get('image_urls', {}).get('original')
            ])
            loader.add_value('referer', response.url)
            yield loader.load_item()
