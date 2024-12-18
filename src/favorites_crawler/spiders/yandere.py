from __future__ import annotations

import pathlib
from urllib.parse import urlencode

from scrapy import Request
from scrapy.exceptions import CloseSpider

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.constants.domains import YANDERE_DOMAIN
from favorites_crawler.itemloaders import YanderePostItemLoader
from favorites_crawler.constants.endpoints import YANDERE_LIST_POST_URL, YANDERE_SHOW_POST_URL
from favorites_crawler.utils.files import list_yandere_post


class YandereSpider(BaseSpider):
    """Crawl voted post from yandere"""
    name = 'yandere'
    allowed_domains = (YANDERE_DOMAIN, )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.PicturePipeline': 0},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = 100
        self.params = {'page': 1, 'limit': self.limit}
        self.posts = {}

    def start_requests(self):
        self.posts = list_yandere_post(pathlib.Path(self.settings.get('FILES_STORE')), include_subdir=True)
        username = self.custom_settings.get('USERNAME')
        if not username:
            raise CloseSpider('login-required')

        self.params['tags'] = f'vote:>=1:{username}'
        yield Request(f'{YANDERE_LIST_POST_URL}?{urlencode(self.params)}')

    def parse_start_url(self, response, **kwargs):
        """Parse list post url"""
        posts = response.json()
        self.close_spider_when_bookmark_not_updated(response, posts=posts)

        if len(posts) == self.limit:
            self.params['page'] += 1
            yield Request(f'{YANDERE_LIST_POST_URL}?{urlencode(self.params)}', callback=self.parse_start_url)

        for post in posts:
            if self.is_crawled(post):
                continue
            loader = YanderePostItemLoader()
            loader.add_value('file_urls', post['file_url'])
            loader.add_value('tags', post['tags'])

            if self.settings.getbool('ENABLE_ORGANIZE_BY_ARTIST'):
                yield Request(YANDERE_SHOW_POST_URL.format(id=post['id']),
                              callback=self.parse, cb_kwargs={'loader': loader})
            else:
                yield loader.load_item()

    def parse(self, response, **kwargs):
        """Parse show post url
        @url https://yande.re/post/show/1056911
        @returns item 1
        @scrapes artist
        """
        loader = kwargs.get('loader', YanderePostItemLoader())
        loader.selector = response
        loader.add_xpath('artist', '//li[@class="tag-type-artist"]/a[last()]/text()')
        yield loader.load_item()

    def is_crawled(self, post: dict) -> bool:
        """Determine whether the post has been crawled, remove old file if filename changed"""
        post_id = str(post['id'])
        if post_id not in self.posts:
            return False
        path = self.posts[post_id]  # type: pathlib.Path
        old_filename = path.name
        new_filename = YanderePostItemLoader.default_item_class().get_filename(post['file_url'], self)
        if new_filename == old_filename:
            return True
        path.unlink(missing_ok=True)
        return False

    def get_last_bookmark_id(self, response, **kwargs):
        posts = kwargs['posts']
        return ','.join(map(lambda x: str(x.get('id')), posts))
