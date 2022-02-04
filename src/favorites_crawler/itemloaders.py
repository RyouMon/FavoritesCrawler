from itemloaders import ItemLoader

from favorites_crawler import items
from favorites_crawler import processors as pc


class PixivIllustItemLoader(ItemLoader):
    """Pixiv Illust Loader"""
    default_item_class = items.PixivIllustItem
    default_output_processor = pc.take_first

    original_image_urls_out = pc.identity
    tags_out = pc.filter_pixiv_tags
