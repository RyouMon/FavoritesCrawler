import pytest

from favorites_crawler.utils.text import ascii_tag


@pytest.mark.parametrize('input_, expected', (
        ('', ''),
        (None, ''),
        ('太もも', 'futomomo'),
        ('凪のあすから', 'nagi_noasukara'),
        ('你好', 'ni_hao'),
        ('hello', 'hello'),
))
def test_ascii_tag(input_, expected):
    assert ascii_tag(input_) == expected
