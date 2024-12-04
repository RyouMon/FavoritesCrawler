# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


class PixivAuthorizationMiddleware:
    def process_request(self, request, spider):
        request.headers.setdefault(b'Authorization', f'Bearer {spider.access_token}')
