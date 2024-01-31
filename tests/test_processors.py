from datetime import datetime, timezone

import pytest

from favorites_crawler import processors
from favorites_crawler.processors import tweet_time_2_datetime


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
        ('[xxxx] xxxx xxx [With Digital Bonus] | xxx[xxx] [Digital] [Uncensored]', 'xxxx xxx'),
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


@pytest.mark.parametrize('url,expected', (
        ('https://www.xxx.com/811102.html#anchor-comment-3423', 1),
        ('https://www.xxx.com/811102.html', 1),
        ('https://www.xxx.com/811102.html/2', 2),
        ('https://www.xxx.com/811102.html/02', 2),
        ('https://www.xxx.com/811102.html/3', 3),
))
def test_get_page(url, expected):
    actual = processors.get_lemon_page(url)
    assert actual == expected


@pytest.mark.parametrize('tags, expected', (
        (
                [
                    {'name': '太もも', 'translated_name': 'thighs'},
                ],
                [
                    'futomomo', 'thighs',
                ],
        ),
))
def test_get_pixiv_tags(tags, expected):
    actual = sorted(processors.get_pixiv_tags(tags))
    assert actual == expected


@pytest.mark.parametrize('tags, expected', (
        (
                ['凪のあすから', 'nagiasu', 'nagi no asu kara'],
                sorted(['nagi_noasukara', 'nagiasu', 'nagi_no_asu_kara']),
        ),
        (
            [], [],
        )
))
def test_get_twitter_tags(tags, expected):
    actual = sorted(processors.get_twitter_tags(tags))
    assert actual == expected


@pytest.mark.parametrize('url, expected', (
        ('https://pbs.twimg.com/media/x.jpg', 'https://pbs.twimg.com/media/x.jpg?name=orig'),
        (None, None),
        ('', ''),
))
def test_fix_tweet_media_url(url, expected):
    actual = processors.fix_tweet_media_url(url)
    assert actual == expected


@pytest.mark.parametrize('tweet_time, expected', (
        ('Sat Oct 20 09:47:03 +0000 2012', datetime(2012, 10, 20, 9, 47, 3, tzinfo=timezone.utc)),
))
def test_tweet_time_2_datetime(tweet_time, expected):
    actual = tweet_time_2_datetime(tweet_time)
    assert actual == expected
