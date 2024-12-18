from unittest.mock import patch

import pytest

from favorites_crawler.spiders.pixiv import PixivSpider
from favorites_crawler.utils.config import load_config


class TestPixivSpider:
    @pytest.mark.parametrize('url, expected', (
            (
                'https://localhost/v1/user/bookmarks/illust?user_id=user_id&restrict=&filter=&max_bookmark_id=1',
                '1'
            ),
            (
                'https://localhost/v1/user/bookmarks/illust?user_id=user_id&restrict=&filter=',
                None
            ),
            (
                'https://localhost/v1/user/bookmarks/illust?user_id=user_id&restrict=&filter=&max_bookmark_id=',
                None
            ),
            (
                None,
                None
            ),
            (
                '',
                None
            )
    ))
    def test_get_max_bookmark_id(self, url, expected):
        actual = PixivSpider.get_max_bookmark_id(url)
        assert actual == expected

    @patch('favorites_crawler.spiders.pixiv.get_favors_home')
    def test_update_mark_id(self, mock_get_favors_name, tmp_path):
        mock_get_favors_name.return_value = tmp_path
        spider = PixivSpider()
        spider.last_bookmark_id = '1'

        spider.update_bookmark_id(None)
        assert spider.last_bookmark_id == '1'

        spider.update_bookmark_id('2')
        assert spider.last_bookmark_id_updated
        assert spider.last_bookmark_id == '2'
        assert load_config(tmp_path)[PixivSpider.name]['LAST_BOOKMARK_ID'] == '2'

        spider.update_bookmark_id('3')
        assert spider.last_bookmark_id == '2'
