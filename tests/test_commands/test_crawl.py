from unittest.mock import patch, MagicMock

import pytest

from favorites_crawler.commands.crawl import spider_closed


@patch('favorites_crawler.commands.crawl.Panel')
def test_spider_closed_should_show_warning(mock_panel):
    mock_spider = MagicMock()
    mock_spider.crawler.stats.get_stats.return_value = {}

    spider_closed(mock_spider)

    mock_panel.assert_called_once()


@patch('favorites_crawler.commands.crawl.Panel')
@pytest.mark.parametrize('item_scrapped_count,item_dropped_count', ((1, 0), (0, 1), (1, 1)))
def test_spider_closed_should_not_show_warning(mock_panel, item_scrapped_count, item_dropped_count):
    mock_spider = MagicMock()
    stats = {'item_scraped_count': item_scrapped_count, 'item_dropped_count': item_dropped_count}
    mock_spider.crawler.stats.get_stats.return_value = {k: v for k, v in stats.items() if v}

    spider_closed(mock_spider)

    mock_panel.assert_not_called()
