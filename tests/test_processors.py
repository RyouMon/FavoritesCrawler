from favorites_crawler import processors


def test_original_url_from_nhentai_thumb_url():
    result = processors.original_url_from_nhentai_thumb_url('https://t2.nhentai.net/galleries/154829234522/4t.png')
    expect = 'https://i2.nhentai.net/galleries/154829234522/4.png'
    assert result == expect
