import json
from urllib.parse import urlencode

from scrapy import Request

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.itemloaders import TwitterTweetItemLoader
from favorites_crawler.constants.domains import TWITTER_DOMAIN
from favorites_crawler.constants.endpoints import TWITTER_LIKES_URL
from favorites_crawler.utils.cookies import load_cookie
from favorites_crawler.utils.common import DictRouter


class TwitterSpider(BaseSpider):
    """Crawl user likes media in twitter"""
    name = 'twitter'
    allowed_domains = [TWITTER_DOMAIN]
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'ITEM_PIPELINES': {'favorites_crawler.pipelines.PicturePipeline': 0},
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
        self.cookies = load_cookie(TWITTER_DOMAIN)
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
        self.features = {
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False, "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "articles_preview_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        }
        self.headers = {
            'Authorization': self.custom_settings.get('AUTHORIZATION'),
            'x-csrf-token': self.custom_settings.get('X_CSRF_TOKEN'),
        }

    def start_requests(self):
        yield Request(self.current_url, headers=self.headers, cookies=self.cookies)

    def parse_start_url(self, response, **kwargs):
        for item_or_request in self.parse(response, **kwargs):
            yield item_or_request

    def parse(self, response, **kwargs):
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
