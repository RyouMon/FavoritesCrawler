from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

from favorites_crawler import items
from favorites_crawler.processors import take_first, identity, get_nhentai_id, original_url_from_nhentai_thumb_url
from favorites_crawler.processors import replace_space_with_under_scope


class PixivIllustItemLoader(ItemLoader):
    """Pixiv Illust Loader"""
    default_item_class = items.PixivIllustItem
    default_output_processor = take_first

    image_urls_out = identity


class YanderePostItemLoader(ItemLoader):
    """Yandere Post Loader"""
    default_item_class = items.YanderePostItem
    default_output_processor = take_first

    image_urls_out = identity


class NHentaiGalleryItemLoader(ItemLoader):
    default_item_class = items.NHentaiGalleryItem
    default_output_processor = take_first

    id_out = Compose(take_first, get_nhentai_id)
    title_out = Join('')
    image_urls_out = MapCompose(original_url_from_nhentai_thumb_url)
    tags_out = MapCompose(replace_space_with_under_scope)
    characters_out = MapCompose(replace_space_with_under_scope)


class LemonPicPostItemLoader(ItemLoader):
    default_item_class = items.LemonPicPostItem
    default_output_processor = take_first

    image_urls_out = identity
    tags_out = identity
