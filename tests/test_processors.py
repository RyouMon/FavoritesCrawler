import pytest

from favorites_crawler import processors


def test_original_url_from_nhentai_thumb_url():
    result = processors.original_url_from_nhentai_thumb_url('https://t2.nhentai.net/galleries/154829234522/4t.png')
    expect = 'https://i2.nhentai.net/galleries/154829234522/4.png'
    assert result == expect


@pytest.mark.parametrize('title,expected', (
    (None, ''),
    ('Hat*** *** t*** | 発********', 'Hat*** *** t***'),
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
    (('(IDOL STAR FESTIV@L 09) [内向***** (るん)] ', 'HLRQ', ' (アイドルマスター ミリオンライブ!)'), 'HLRQ'),
    (('[***] ', 'F**** B***', ' [Digital]'), 'F**** B***'),
    (('[ (**さゆ)] ', '****カルトの儀式', ' [英訳]'), '****カルトの儀式'),
    (('[オレ**] ', '****のお姉さん', ' [DL版]'), '****のお姉さん'),
    (('(COMIC1☆9) [*** *** (***)] ', 'Seifuku ******** 7', ''), 'Seifuku ******** 7'),
    (('(*** Summer) [** (飴玉コン)] ', 'confiture ***vol.13', ' (ご注文はうさぎですか?)'), 'confiture ***vol.13'),
    (('(C82) [SK*** (SK***)] ', '千反田*****', ' (氷菓)'), '千反田*****'),
))
def test_select_best_nhentai_title(titles, expected):
    actual = processors.select_best_nhentai_title(titles)

    assert actual == expected


def test_get_year():
    actual = processors.get_year_from_iso_format('2022-08-03T00:06:46.533158+00:00')

    assert actual == 2022


def test_get_month():
    actual = processors.get_month_from_iso_format('2022-08-03T00:06:46.533158+00:00')

    assert actual == 8


@pytest.mark.parametrize('title,expected', (
    ('confiture あ****ン', None),
    ('confiture あ****ンvol.7', 7),
    ('confiture あ****ンvol.13', 13),
    ('S**** S**** 7', 7),
    ('S**** S**** 13', 13),
))
def test_get_volume_from_title(title, expected):
    actual = processors.get_volume_from_title(title)

    assert actual == expected


@pytest.mark.parametrize('title,expected', (
    ('confiture あ****ン', None),
    ('confiture あ****ンvol.7', 'confiture あ****ン'),
    ('confiture あ****ンvol.13', 'confiture あ****ン'),
    ('confiture あ****ン vol.13', 'confiture あ****ン'),
    ('S**** S**** 7', 'S**** S****'),
    ('S**** S**** 13', 'S**** S****'),
))
def test_get_series_from_title(title, expected):
    actual = processors.get_series_from_title(title)

    assert actual == expected


@pytest.mark.parametrize('parodies,expected', (
    ('', None), (None, None),
    (' [中国翻訳]', None),
    (' (ご注文はうさぎですか?)', 'ご注文はうさぎですか?'),
    ('gochuumon wa usagi desu ka | is the order a rabbit', 'gochuumon wa usagi desu ka'),
    ('gochuumon wa usagi desu ka', 'gochuumon wa usagi desu ka'),
    (' gochuumon wa usagi desu ka ', 'gochuumon wa usagi desu ka'),
    (' (化物語) [DL版]', '化物語'),
))
def test_clean_parodies(parodies, expected):
    actual = processors.clean_parodies(parodies)

    assert actual == expected
