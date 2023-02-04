from unittest.mock import patch, sentinel, MagicMock, call

import pytest
from scrapy.exceptions import DropItem

from favorites_crawler.pipelines import FavoritesFilePipeline


class TestFavoritesFilePipeline:

    def test_process_item_should_drop_item_when_cbz_file_already_exist(self, tmp_path):
        (tmp_path / 'abc.cbz').touch()
        mock_item = MagicMock()
        mock_item.get_folder_name.return_value = 'abc'

        with pytest.raises(DropItem):
            FavoritesFilePipeline(str(tmp_path)).process_item(mock_item, None)

    @patch('favorites_crawler.pipelines.Request')
    def test_should_set_referer_when_get_media_requests(self, mock_request):
        mock_item = {'referer': sentinel.referer, 'file_urls': [getattr(sentinel, f'url-{i}') for i in range(1, 10)]}

        list(FavoritesFilePipeline('mock_path').get_media_requests(mock_item, None))

        calls = [
            call(getattr(sentinel, f'url-{i}'), headers={'referer': sentinel.referer})
            for i in range(1, 10)
        ]
        mock_request.assert_has_calls(calls, any_order=True)

    def test_file_path_should_call_item_get_filepath(self):
        mock_request = MagicMock()
        mock_info = MagicMock()
        mock_item = MagicMock()

        FavoritesFilePipeline('mock_path').file_path(mock_request, None, mock_info, item=mock_item)

        mock_item.get_filepath.assert_called_once_with(mock_request.url, mock_info.spider)

    @patch('favorites_crawler.pipelines.create_comic_archive')
    def test_should_create_comic_archive_when_close_spider(self, mock_create_comic_archive, tmp_path):
        pipeline = FavoritesFilePipeline('mock_path')
        pipeline.files_path = tmp_path
        pipeline.comic_comments = {'comic': b'comment'}

        pipeline.close_spider(None)

        mock_create_comic_archive.assert_called_once_with(tmp_path / 'comic', comment=b'comment')

    @patch('favorites_crawler.pipelines.create_comic_archive')
    def test_should_not_create_comic_archive_when_comic_comments_is_empty(self, mock_create_comic_archive, tmp_path):
        pipeline = FavoritesFilePipeline('mock_path')
        pipeline.comic_comments = {}

        pipeline.close_spider(None)

        mock_create_comic_archive.assert_not_called()
