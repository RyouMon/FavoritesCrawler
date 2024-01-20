from pathlib import Path

import pytest

from favorites_crawler.utils.common import DictRouter
from favorites_crawler.utils.files import load_json


class TestDictRouter:
    @pytest.mark.parametrize('obj, path, default, expected', (
            ({'a': {'b': 1}}, 'a.b', None, 1),
            ({'a': 1}, 'a.b', None, None),
            ({'a': [1]}, 'a.0', None, 1),
            ({'a': []}, 'a.0', None, None),
            ({'a': [{'b': 1}]}, 'a.0.b', None, 1),
            ({'a': [{}]}, 'a.0.b', None, None),
            ({'a': []}, 'a.0.b', None, None),
    ))
    def test_route_to(self, obj, path, default, expected):
        router = DictRouter(obj)
        assert router.route_to(path, default) == expected

    @pytest.mark.parametrize('obj, expr, expected', (
            (
                    {'a': {'b': 1}, 'c': {'b': 2}},
                    '*.b',
                    [1, 2]),
            (
                    {'d': [{'b': 3}, {'b': 4}]},
                    '*[*].b',
                    [3, 4],
            ),
            (
                    {'a': {'b': 1}, 'c': {'b': 2}, 'd': [{'b': 3}, {'b': 4}]},
                    '$..b',
                    [1, 2, 3, 4]
            ),
            (
                    load_json(Path(__file__).parent.parent / 'mock' / 'entry.json'),
                    '$..media_url_https',
                    [
                        'https://pbs.twimg.com/media/GDhrZulbMAAxh1l.jpg',
                        'https://pbs.twimg.com/media/GDhrZulbMAAxh1l.jpg',
                    ],
            ),
    ))
    def test_find(self, obj, expr, expected):
        router = DictRouter(obj)
        assert router.find(expr) == expected

