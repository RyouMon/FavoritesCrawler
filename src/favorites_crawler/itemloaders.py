from itemloaders import ItemLoader
from itemloaders.processors import Join

from favorites_crawler import items
from favorites_crawler.processors import take_first, identity, filter_pixiv_tags


class PixivIllustItemLoader(ItemLoader):
    """Pixiv Illust Loader"""
    default_item_class = items.PixivIllustItem
    default_output_processor = take_first

    original_image_urls_out = identity
    tags_out = filter_pixiv_tags


class YanderePostItemLoader(ItemLoader):
    """Yandere Post Loader"""
    default_item_class = items.YanderePostItem
    default_output_processor = take_first


class NHentaiGalleryItemLoader(ItemLoader):
    default_item_class = items.NHentaiGalleryItem
    default_output_processor = take_first

    title_out = Join('')


class LemonPicPostItemLoader(ItemLoader):
    default_item_class = items.LemonPicPostItem
    default_output_processor = take_first

    image_urls_out = identity
    tags_out = identity
