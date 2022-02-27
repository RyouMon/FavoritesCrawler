import os.path
from urllib.parse import unquote

from scrapy import Item, Field

from favorites_crawler.utils.text import drop_illegal_characters


class BaseItem(Item):
    id = Field()
    title = Field()
    image_urls = Field()
    tags = Field()
    referer = Field()

    def get_filepath(self, url):
        folder_name = self.get_folder_name()
        filename = self.get_filename(url)
        filepath = os.path.join(folder_name, filename)
        return drop_illegal_characters(filepath)

    def get_filename(self, url):
        return unquote(url.rsplit('/', maxsplit=1)[1])

    def get_folder_name(self):
        name = self.get('title', '')
        prefix = self.get_folder_prefix()
        subfix = self.get_folder_subfix()
        return f'{prefix}{name}{subfix}'

    def get_folder_prefix(self):
        return f'[{self.get("id", "")}] '

    def get_folder_subfix(self):
        tags = ' '.join(self.get('tags', ()))
        if not tags:
            return ''
        return f' [{tags}]'


class PixivIllustItem(BaseItem):

    def get_folder_name(self):
        return ''


class YanderePostItem(BaseItem):
    """Yandere Post"""

    def get_folder_name(self):
        return ''


class LemonPicPostItem(BaseItem):

    def get_folder_prefix(self):
        return ''


class NHentaiGalleryItem(BaseItem):
    characters = Field()

    def get_folder_name(self):
        characters = ' '.join(self.get('characters', ()))
        prefix = f'[{self.get("id", "")}] {self.get("title", "")}'
        if characters:
            return prefix + f' [{characters}]'
        return prefix
