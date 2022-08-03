from datetime import date
from unittest.mock import patch

import pytest

from favorites_crawler import items


class TestBaseItem:

    @pytest.mark.parametrize('url,expected', (
        ('https://mock.domain/path/1.jpg', '1.jpg'),
        ('https://mock.domain/path/1.png', '1.png'),
        ('https://mock.domain/path/1.jpeg', '1.jpeg'),
    ))
    def test_get_filename(self, url, expected):
        item = items.BaseItem()

        actual = item.get_filename(url)

        assert actual == expected

    def test_get_folder_name_should_return_title(self):
        item = items.BaseItem()
        item.title = 'abc'

        actual = item.get_folder_name()

        assert actual == item.title

    @patch('favorites_crawler.items.datetime')
    def test_get_folder_name_should_return_iso_date_when_title_is_none(self, mock_datetime):
        mock_today = mock_datetime.date.today
        mock_today.return_value = date(2022, 2, 3)
        item = items.BaseItem()
        item.title = None

        actual = item.get_folder_name()

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
