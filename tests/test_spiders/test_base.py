from unittest.mock import patch

from favorites_crawler.spiders import BaseSpider
from favorites_crawler.utils.config import load_config


class TestBaseSpider:
    @patch('favorites_crawler.spiders.get_favors_home')
    def test_update_bookmark_id(self, mock_get_favors_name, tmp_path):
        mock_get_favors_name.return_value = tmp_path
        spider = BaseSpider('test')
        spider.last_bookmark_id = '1'

        spider.update_last_bookmark_id(None)
        assert spider.last_bookmark_id == '1'

        spider.update_last_bookmark_id('2')
        assert spider.last_bookmark_id_updated
        assert spider.last_bookmark_id == '2'
        assert load_config(tmp_path)[spider.name]['LAST_BOOKMARK_ID'] == '2'

        spider.update_last_bookmark_id('3')
        assert spider.last_bookmark_id == '2'
