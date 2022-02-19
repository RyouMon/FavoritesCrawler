from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose

from favorites_crawler import items
from favorites_crawler.processors import take_first, identity, filter_pixiv_tags, get_nhentai_id


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

    id_out = Compose(take_first, get_nhentai_id)
    title_out = Join('')
    image_urls_out = identity


class LemonPicPostItemLoader(ItemLoader):
    default_item_class = items.LemonPicPostItem
    default_output_processor = take_first

    image_urls_out = identity
    tags_out = identity
