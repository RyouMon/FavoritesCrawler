import json
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

    @patch('favorites_crawler.items.date')
    def test_get_folder_name_should_return_iso_date_when_title_is_none(self, mock_date):
        mock_today = mock_date.today
        mock_today.return_value = date(2022, 2, 3)
        item = items.BaseItem()
        item.title = None

        actual = item.get_folder_name(None)

        assert actual == '2022-02-03'


@pytest.fixture
def comic_book_info():
    return {
        'id': 1,
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
    def test_to_comic_info_should_not_contains_null(self):
        item = items.ComicBookInfoItem()

        result = json.dumps(item.get_comic_info())

        assert '"null"' not in result

    @patch('favorites_crawler.items.datetime')
    def test_to_comic_info(self, mock_datetime, comic_book_info):
        mock_now = mock_datetime.now
        mock_now.return_value = 'test'
        item = items.ComicBookInfoItem(**comic_book_info)

        result = item.get_comic_info()

        assert result == {
            'ComicBookInfo/1.0': {
                'comments': 'Tales of the Black Freighter...',
                'country': 'United States',
                'credits': [
                    {'person': 'Moore, Alan', 'role': 'Writer'},
                    {'person': 'Gibbons, Dave', 'role': 'Artist'}
                ],
                'genre': 'Superhero',
                'issue': 1,
                'language': 'English',
                'numberOfIssues': 12,
                'numberOfVolumes': 1,
                'publicationMonth': 9,
                'publicationYear': 1986,
                'publisher': 'DC Comics',
                'rating': 5,
                'series': 'Watchmen',
                'tags': ['Rorschach', 'Ozymandias', 'Nite Owl'],
                'title': 'At Midnight, All the Agents',
                'volume': 1
            },
            'appID': 'FavoritesCrawler',
            'lastModified': 'test',
            'x-FavoritesCrawler': {'id': 1}
        }


class TestNHentaiGalleryItem:
    @patch('favorites_crawler.items.datetime')
    def test_to_comic_info(self, mock_datetime, comic_book_info):
        mock_now = mock_datetime.now
        mock_now.return_value = 'test'
        item = items.NHentaiGalleryItem(**comic_book_info)

        result = item.get_comic_info()

        assert result == {
            'ComicBookInfo/1.0': {
                'comments': 'Tales of the Black Freighter...',
                'country': 'United States',
                'credits': [
                    {'person': 'Moore, Alan', 'role': 'Writer'},
                    {'person': 'Gibbons, Dave', 'role': 'Artist'}
                ],
                'genre': 'Superhero',
                'issue': 1,
                'language': 'English',
                'numberOfIssues': 12,
                'numberOfVolumes': 1,
                'publicationMonth': 9,
                'publicationYear': 1986,
                'publisher': 'DC Comics',
                'rating': 5,
                'series': 'Watchmen',
                'tags': ['Rorschach', 'Ozymandias', 'Nite Owl'],
                'title': 'At Midnight, All the Agents',
                'volume': 1
            },
            'appID': 'FavoritesCrawler',
            'lastModified': 'test',
            'x-FavoritesCrawler': {'id': 1}
        }


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
