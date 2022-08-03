from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

from favorites_crawler import items
from favorites_crawler.processors import take_first, identity, get_nhentai_id, wrap_credits, \
    original_url_from_nhentai_thumb_url, select_best_nhentai_title, clean_nhentai_title, \
    get_year_from_iso_format, get_month_from_iso_format, get_series_from_title, get_volume_from_title, \
    clean_parodies


class PixivIllustItemLoader(ItemLoader):
    """Pixiv Illust Loader"""
    default_item_class = items.PixivIllustItem
    default_output_processor = take_first

    file_urls_out = identity


class YanderePostItemLoader(ItemLoader):
    """Yandere Post Loader"""
    default_item_class = items.YanderePostItem
    default_output_processor = take_first

    file_urls_out = identity


class NHentaiGalleryItemLoader(ItemLoader):
    default_item_class = items.NHentaiGalleryItem
    default_output_processor = take_first

    id_out = Compose(take_first, get_nhentai_id)
    parodies_out = Compose(take_first, clean_parodies)
    characters_out = identity

    series_out = Compose(take_first, get_series_from_title)
    volume_out = Compose(take_first, get_volume_from_title)
    title_out = Compose(select_best_nhentai_title, clean_nhentai_title)
    sort_title_out = Compose(select_best_nhentai_title, clean_nhentai_title)
    file_urls_out = MapCompose(original_url_from_nhentai_thumb_url)
    credits_out = wrap_credits
    tags_out = identity
    publicationYear_out = Compose(take_first, get_year_from_iso_format)
    publicationMonth_out = Compose(take_first, get_month_from_iso_format)


class LemonPicPostItemLoader(ItemLoader):
    default_item_class = items.LemonPicPostItem
    default_output_processor = take_first

    file_urls_out = identity
    tags_out = identity
