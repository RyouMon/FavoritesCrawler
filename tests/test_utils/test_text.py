import pytest

from favorites_crawler.utils.text import convert_to_ascii


@pytest.mark.parametrize('input_, expected', (
        ('', ''),
        (None, ''),
        ('太もも', 'futomomo'),
        ('凪のあすから', 'nagi_noasukara'),
        ('你好', 'ni_hao'),
        ('hello', 'hello'),
))
def test_convert_to_ascii(input_, expected):
    assert convert_to_ascii(input_) == expected
