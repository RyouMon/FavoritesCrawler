import pytest

from favorites_crawler.commands.login import parse_twitter_likes_url


@pytest.mark.parametrize('url, expected', (
        (
                'https://twitter.com/i/api/graphql/xxxx/Likes?variables=%7B%22userId%22%3A%22xxxx%22%2C%22...',
                ('xxxx', 'xxxx'),
        ),
))
def test_twitter_parse_likes_url(url, expected):
    assert parse_twitter_likes_url(url) == expected
