from pathlib import Path

from scrapy import FormRequest

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.constants.domains import YANDERE_DOMAIN
from favorites_crawler.constants.endpoints import YANDERE_VOTE_POST_URL
from favorites_crawler.utils.files import list_yandere_id


class YandereVoteSpider(BaseSpider):
    """Vote yandere post"""
    name = 'yandere_vote'
    allowed_domains = (YANDERE_DOMAIN, )
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
    }

    def __init__(self, csrf_token, cookie, score, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookies = {}
        for pair in cookie.split('; '):
            k, v = pair.split('=')
            self.cookies[k] = v
        self.headers = {'x-csrf-token': csrf_token}
        self.score = score
        self.path = Path(path)

    def start_requests(self):
        yandere_id_list = list_yandere_id(self.path)
        self.crawler.stats.set_value('file_count', len(yandere_id_list))
        yandere_id_set = set(yandere_id_list)
        self.crawler.stats.set_value('voted/expected', len(yandere_id_set))

        for i in yandere_id_set:
            yield FormRequest(YANDERE_VOTE_POST_URL,
                              formdata={'id': str(i), 'score': str(self.score)},
                              cookies=self.cookies, headers=self.headers,
                              callback=self.parse)

    def parse(self, response, **kwargs):
        self.crawler.stats.inc_value('voted/count')
