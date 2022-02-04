# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from favorites_crawler.utils.auth import refresh_pixiv


class PixivAuthorizationMiddleware:
    def __init__(self):
        self.access_token = refresh_pixiv()

    def process_request(self, request, spider):
        if self.access_token:
            request.headers.setdefault(b'Authorization', f'Bearer {self.access_token}')
