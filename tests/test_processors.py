import pytest

from favorites_crawler import processors


def test_original_url_from_nhentai_thumb_url():
    result = processors.original_url_from_nhentai_thumb_url('https://t2.nhentai.net/galleries/154829234522/4t.png')
    expect = 'https://i2.nhentai.net/galleries/154829234522/4.png'
    assert result == expect


@pytest.mark.parametrize('title,expected', (
    (None, ''),
    ('(THE IDOLM@STER MILLION LIVE!)', 'THE IDOLM@STER MILLION LIVE!'),
    ('Funky Baby', 'Funky Baby'),
    ('Event no Retsu de...', 'Event no Retsu de'),
    ('Event no Retsu de..', 'Event no Retsu de'),
    ('Event no Retsu de.', 'Event no Retsu de'),
))
def test_clean_nhentai_title(title, expected):
    actual = processors.clean_nhentai_title(title)

    assert actual == expected


@pytest.mark.parametrize('titles,expected', (
    (None, ''),
    (('', '', ''), ''),
    (('(IDOL STAR FESTIV@L 09) [内向***** (るん)] ', 'HLRQ', ' (アイドルマスター ミリオンライブ!)'), '(アイドルマスター ミリオンライブ!)'),
    (('F**** Baby', '', ''), 'F**** Baby'),
    (('[ (**さゆ)] ', '****カルトの儀式', ' [英訳]'), '****カルトの儀式'),
    (('[オレ**] ', '****のお姉さん', ' [DL版]'), '****のお姉さん'),
    (('(COMIC1☆9) [*** *** (***)] ', 'Seifuku ******** 7', ''), 'Seifuku ******** 7'),
))
def test_select_best_nhentai_title(titles, expected):
    actual = processors.select_best_nhentai_title(titles)

    assert actual == expected
