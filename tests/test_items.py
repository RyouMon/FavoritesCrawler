from datetime import date
from unittest.mock import patch, MagicMock

import pytest

from favorites_crawler import items


class TestBaseItem:
    @pytest.mark.parametrize('url,expected', (
        ('https://mock.domain/path/1.jpg', '1.jpg'),
        ('https://mock.domain/path/1.png', '1.png'),
        ('https://mock.domain/path/1.jpeg', '1.jpeg'),
        ('https://mock.domain/1.jpeg', '1.jpeg'),
    ))
    def test_get_filename(self, url, expected):
        item = items.BaseItem()

        actual = item.get_filename(url, None)

        assert actual == expected

    def test_get_folder_name_should_return_title(self):
        item = items.BaseItem()
        item.title = 'abc'

        actual = item.get_folder_name(None)

        assert actual == item.title

    @patch('favorites_crawler.items.datetime')
    def test_get_folder_name_should_return_iso_date_when_title_is_none(self, mock_datetime):
        mock_today = mock_datetime.date.today
        mock_today.return_value = date(2022, 2, 3)
        item = items.BaseItem()
        item.title = None

        actual = item.get_folder_name(None)

        assert actual == '2022-02-03'


@pytest.fixture
def comic_book_info():
    return {
        'series': 'Watchmen',
        'title': 'At Midnight, All the Agents',
        'publisher': 'DC Comics',
        'publicationMonth': 9,
        'publicationYear': 1986,
        'issue': 1,
        'numberOfIssues': 12,
        'volume': 1,
        'numberOfVolumes': 1,
        'rating': 5,
        'genre': 'Superhero',
        'language': 'English',
        'country': 'United States',
        'credits': [
            {'person': 'Moore, Alan', 'role': 'Writer'},
            {'person': 'Gibbons, Dave', 'role': 'Artist'},
        ],
        'tags': ['Rorschach', 'Ozymandias', 'Nite Owl'],
        'comments': 'Tales of the Black Freighter...',
    }


class TestComicBookInfoItem:
    @patch('favorites_crawler.items.json')
    def test_to_comic_info_should_call_json(self, mock_json, comic_book_info):
        mock_dumps = mock_json.dumps
        item = items.ComicBookInfoItem(**comic_book_info)

        actual = item.get_comic_info()

        mock_dumps.assert_called_once()
        assert actual == mock_dumps.return_value

    def test_to_comic_info(self, comic_book_info):
        item = items.NHentaiGalleryItem(**comic_book_info)

        result = item.get_comic_info()

        assert '"appID"' in result
        assert '"appID"' in result
        assert '"lastModified"' in result
        assert '"ComicBookInfo/1.0"' in result

    def test_to_comic_info_should_not_contains_null(self):
        item = items.NHentaiGalleryItem()

        result = item.get_comic_info()

        assert '"null"' not in result


class TestNHentaiGalleryItem:
    def test_to_comic_info(self, comic_book_info):
        item = items.NHentaiGalleryItem(**comic_book_info)

        result = item.get_comic_info()

        assert '"ComicBookInfo/1.0"' in result
        assert '"file_urls"' not in result
        assert '"id"' not in result
        assert '"referer"' not in result


class TestPixivIllustItem:
    def test_get_folder_name_should_return_empty_when_disable_organize_by_user(self):
        mock_spider = MagicMock()
        mock_spider.crawler.settings.getbool.return_value = False
        item = items.PixivIllustItem()

        actual = item.get_folder_name(mock_spider)

        assert actual == ''

    @pytest.mark.parametrize('user_id,expected', (
            (None, 'unknown'),
            ('', 'unknown'),
            ('123456', '123456'),
    ))
    def test_get_folder_name_should_return_user_id_when_enable_organize_by_user(self, user_id, expected):
        mock_spider = MagicMock()
        mock_spider.crawler.settings.getbool.return_value = True
        item = items.PixivIllustItem(user_id=user_id)

        actual = item.get_folder_name(mock_spider)

        assert actual == expected


class TestTwitterTweetItem:
    @pytest.mark.parametrize('username, expected', (
            (None, 'unknown'),
            ('', 'unknown'),
            ('someone', 'someone'),
    ))
    def test_get_folder_name(self, username, expected):
        mock_spider = MagicMock()
        mock_spider.crawler.settings.getbool.return_value = True
        item = items.TwitterTweetItem(username=username)

        actual = item.get_folder_name(mock_spider)

        assert actual == expected

    @pytest.mark.parametrize('id_, url, expected', (
            (1, 'https://pbs.twimg.com/media/xGDYpKX8bMAANM-J.jpg?name=orig', '1 xGDYpKX8bMAANM-J.jpg'),
            (1, 'https://pbs.twimg.com/media/xGDYpKX8bMAANM-J.jpg', '1 xGDYpKX8bMAANM-J.jpg'),
    ))
    def test_get_filename(self, id_, url, expected):
        item = items.TwitterTweetItem(id=id_)

        actual = item.get_filename(url, None)

        assert actual == expected
