from functools import partial

from itemloaders import ItemLoader
from itemloaders.processors import Compose, MapCompose

from favorites_crawler import items
from favorites_crawler.processors import take_first, identity, get_nhentai_id, wrap_credits, \
    original_url_from_nhentai_thumb_url, select_best_nhentai_title, clean_nhentai_title, \
    get_year_from_iso_format, get_month_from_iso_format, get_series_from_title, get_volume_from_title, \
    clean_parodies, get_lemon_page, get_pixiv_tags, get_yandere_tags, get_twitter_tags, fix_tweet_media_url, \
    tweet_time_2_datetime
from favorites_crawler.utils.text import convert_to_ascii


convert_to_ascii = partial(convert_to_ascii, replace_space=False)


class BaseItemLoader(ItemLoader):
    default_output_processor = take_first

    file_urls_out = identity
    tags_out = identity


class PixivIllustItemLoader(BaseItemLoader):
    default_item_class = items.PixivIllustItem

    user_id_out = Compose(take_first, str)
    tags_out = get_pixiv_tags
    title_out = Compose(take_first, convert_to_ascii)


class YanderePostItemLoader(BaseItemLoader):
    default_item_class = items.YanderePostItem

    artist_out = Compose(take_first, lambda s: s.strip())
    tags_out = Compose(take_first, get_yandere_tags)


class NHentaiGalleryItemLoader(BaseItemLoader):
    default_item_class = items.NHentaiGalleryItem

    id_out = Compose(take_first, get_nhentai_id)
    parodies_out = Compose(take_first, clean_parodies)
    characters_out = identity
    series_out = Compose(take_first, get_series_from_title)
    volume_out = Compose(take_first, get_volume_from_title)
    title_out = Compose(select_best_nhentai_title, clean_nhentai_title)
    sort_title_out = Compose(select_best_nhentai_title, clean_nhentai_title)
    file_urls_out = MapCompose(original_url_from_nhentai_thumb_url)
    credits_out = wrap_credits
    publicationYear_out = Compose(take_first, get_year_from_iso_format)
    publicationMonth_out = Compose(take_first, get_month_from_iso_format)


class LemonPicPostItemLoader(BaseItemLoader):
    default_item_class = items.LemonPicPostItem

    page_out = Compose(take_first, get_lemon_page)


class TwitterTweetItemLoader(BaseItemLoader):
    default_item_class = items.TwitterTweetItem

    tags_out = get_twitter_tags
    file_urls_out = MapCompose(fix_tweet_media_url)
    created_time_out = Compose(take_first, tweet_time_2_datetime)
