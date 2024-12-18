from pathlib import Path

from favorites_crawler.spiders.yandere import YandereSpider


class TestYandereSpider:
    def test_is_crawled_return_false_if_post_not_crawled(self):
        spider = YandereSpider()
        post = {'id': 1}

        is_crawled = spider.is_crawled(post)

        assert is_crawled is False

    def test_is_crawled_return_true_if_post_crawled_and_filename_not_changed(self):
        spider = YandereSpider()
        spider.posts['1'] = Path() / 'test.jpg'
        post = {'id': 1, 'file_url': '/test.jpg'}

        is_crawled = spider.is_crawled(post)

        assert is_crawled is True

    def test_is_crawled_return_false_if_post_crawled_and_filename_changed(self, tmp_path):
        spider = YandereSpider()
        old_file = tmp_path / 'test.jpg'
        spider.posts['1'] = old_file
        old_file.touch()
        assert old_file.exists()
        post = {'id': 1, 'file_url': '/nameChanged.jpg'}

        is_crawled = spider.is_crawled(post)

        assert is_crawled is False
        assert not old_file.exists()
