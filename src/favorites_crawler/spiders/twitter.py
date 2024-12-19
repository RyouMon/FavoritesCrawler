import json
from urllib.parse import urlencode

from scrapy import Request

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import TwitterTweetItemLoader
from favorites_crawler.constants.domains import TWITTER_DOMAIN
from favorites_crawler.constants.endpoints import TWITTER_LIKES_URL
from favorites_crawler.utils.common import DictRouter


class TwitterSpider(BaseSpider):
    """Crawl user likes media in twitter"""
    name = 'twitter'
    allowed_domains = [TWITTER_DOMAIN]
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.PicturePipeline': 0},
        'HTTPERROR_ALLOWED_CODES': [400],
    }

    @property
    def current_url(self):
        query = urlencode({
            'variables': json.dumps(self.variables),
            'features': json.dumps(self.features),
        })
        return self.base_url + '?' + query

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = TWITTER_LIKES_URL.format(id=self.custom_settings.get('LIKES_ID'))
        self.variables = {
            "userId": str(self.custom_settings.get('USER_ID')),
            "count": 100,
            "includePromotedContent": False,
            "withClientEventToken": False,
            "withBirdwatchNotes": False,
            "withVoice": True,
            "withV2Timeline": True
        }
        self.features = self.custom_settings.get('FEATURES', {})
        self.headers = {
            'Authorization': self.custom_settings.get('AUTHORIZATION'),
            'x-csrf-token': self.custom_settings.get('X_CSRF_TOKEN'),
        }

    def start_requests(self):
        yield Request(self.current_url, headers=self.headers, cookies=self.cookies)

    def parse_start_url(self, response, **kwargs):
        self.close_spider_when_bookmark_not_updated(response, **kwargs)
        yield from self.parse(response, **kwargs)

    def parse(self, response, **kwargs):
        if response.status == 400:
            self.logger.error('Failed to request x API, error message: %s', response.json())

        entries = (
            entry['content'] for entry in DictRouter(response.json()).route_to(
            'data.user.result.timeline_v2.timeline.instructions.0.entries', [],
        ))
        cursor_value = None
        timeline_item_count = 0
        for entry in entries:
            entry_type = entry['entryType']
            if entry_type == 'TimelineTimelineItem':
                timeline_item_count += 1
                for item in self.parse_timeline_item(entry):
                    yield item
            elif entry_type == 'TimelineTimelineCursor' and entry['cursorType'] == 'Bottom':
                cursor_value = entry['value']

        if timeline_item_count and cursor_value:
            self.variables['cursor'] = cursor_value
            yield Request(self.current_url, headers=self.headers, cookies=self.cookies)

    def parse_timeline_item(self, entry):
        entry_router = DictRouter(entry)
        loader = TwitterTweetItemLoader()
        loader.add_value('id', entry_router.find('$..rest_id'))
        loader.add_value('username', entry_router.find('$..screen_name'))
        loader.add_value('tags', entry_router.find('$..hashtags[*].text'))
        loader.add_value('file_urls', list(set(entry_router.find('$..media_url_https'))))
        loader.add_value('created_time', entry_router.route_to(
            'itemContent.tweet_results.result.legacy.created_at',
        ))
        yield loader.load_item()

    def get_last_bookmark_id(self, response, **kwargs):
        data = response.json()
        router = DictRouter(data)
        id_list: list = router.find('$..tweet_results.result.rest_id')
        return ','.join(id_list)
