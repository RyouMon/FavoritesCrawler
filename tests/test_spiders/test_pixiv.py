from unittest.mock import MagicMock

import pytest

from favorites_crawler.spiders.pixiv import PixivSpider


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
        spider = PixivSpider()
        mock_response = MagicMock()
        mock_json = mock_response.json
        mock_json.return_value = {'next_url': url}

        actual = spider.get_last_bookmark_id(mock_response)

        assert actual == expected
