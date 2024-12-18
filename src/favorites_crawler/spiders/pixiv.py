from __future__ import annotations

from urllib.parse import urlencode, urlparse, parse_qs

from scrapy import Request
from scrapy.exceptions import CloseSpider

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import PixivIllustItemLoader
from favorites_crawler.constants.domains import PIXIV_DOMAIN
from favorites_crawler.constants.endpoints import PIXIV_USER_BOOKMARKS_ENDPOINT
from favorites_crawler.constants.headers import PIXIV_REQUEST_HEADERS, PIXIV_IOS_USER_AGENT
from favorites_crawler.utils.config import load_config, dump_config
from favorites_crawler.utils.common import get_favors_home


class PixivSpider(BaseSpider):
    """Crawl user bookmarks in pixiv"""
    name = 'pixiv'
    allowed_domains = (PIXIV_DOMAIN, )
    custom_settings = {
        'USER_AGENT': PIXIV_IOS_USER_AGENT,
        'DEFAULT_REQUEST_HEADERS': PIXIV_REQUEST_HEADERS,
        # Add PixivAuthorizationMiddleware after DefaultHeadersMiddleware
        'DOWNLOADER_MIDDLEWARES': {'favorites_crawler.middlewares.PixivAuthorizationMiddleware': 450},
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.PicturePipeline': 0},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_bookmark_id = self.custom_settings.get('LAST_BOOKMARK_ID')
        self.last_bookmark_id_updated = False

    def start_requests(self):
        user_id = self.custom_settings.get('USER_ID')
        if not user_id:
            raise CloseSpider('login-required')

        params = {'user_id': user_id, 'restrict': 'public', 'filter': 'for_ios'}
        yield Request(f'{PIXIV_USER_BOOKMARKS_ENDPOINT}?{urlencode(params)}')

    def parse_start_url(self, response, **kwargs):
        result = response.json()
        last_bookmark_id = self.get_max_bookmark_id(result.get('next_url'))
        if self.last_bookmark_id and (self.last_bookmark_id == last_bookmark_id):
            self.logger.info('Crawled to last bookmark id, close spider.')
            raise CloseSpider('fastly-finished')
        self.update_bookmark_id(last_bookmark_id)

        for request_or_item in self.parse(response, **kwargs):
            yield request_or_item

    def parse(self, response, **kwargs):
        result = response.json()
        next_link = result.get('next_url')
        if next_link:
            yield response.follow(next_link)

        illust_list = result.get('illusts', ())
        for illust in illust_list:
            loader = PixivIllustItemLoader()
            loader.add_value('id', illust.get('id'))
            loader.add_value('title', illust.get('title'))
            loader.add_value('tags', illust.get('tags'))
            loader.add_value('file_urls', illust.get('meta_single_page', {}).get('original_image_url', ()))
            loader.add_value('file_urls', [
                d['image_urls']['original'] for d in illust.get('meta_pages', ())
                if d.get('image_urls', {}).get('original')
            ])
            loader.add_value('user_id', illust.get('user', {}).get('id'))
            loader.add_value('referer', response.url)
            yield loader.load_item()

    @staticmethod
    def get_max_bookmark_id(next_link: str) -> str | None:
        parsed_url = urlparse(next_link)
        query_params = parse_qs(parsed_url.query)
        return query_params.get('max_bookmark_id', [None])[0]

    def update_bookmark_id(self, bookmark_id):
        if not bookmark_id or self.last_bookmark_id_updated:
            return
        self.last_bookmark_id = bookmark_id
        self.last_bookmark_id_updated = True
        favors_home = get_favors_home()
        config = load_config(favors_home)
        config.get(self.name, {})['LAST_BOOKMARK_ID'] = bookmark_id
        dump_config(config, favors_home)
        self.logger.info('Updated LAST_BOOKMARK_ID: %s', bookmark_id)
