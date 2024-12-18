from unittest.mock import MagicMock

from scrapy.spiders.crawl import Link

from favorites_crawler.spiders.nhentai import NHentaiSpider


class TestNhentai:
    def test_filter_exists_comic(self):
        spider = NHentaiSpider()
        spider.comics = {'1': ''}
        spider.crawler = MagicMock()
        links = [
            Link(url='https://xxx/1/'),
            Link(url='https://xxx/11/')
        ]

        links = spider.filter_exists_comics(links)

        assert links == [
            Link(url='https://xxx/11/')
        ]
