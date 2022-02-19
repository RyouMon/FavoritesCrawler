import os.path
from typing import List
from urllib.parse import unquote
from dataclasses import dataclass, field

from favorites_crawler.utils.text import drop_illegal_characters


@dataclass
class BaseItem:
    id: int = field(default=None)
    title: str = field(default=None)
    image_urls: List = field(default_factory=list)
    tags: List = field(default_factory=list)
    referer: str = field(default=None)

    def get_filepath(self, url):
        folder_name = self.get_folder_name()
        filename = self.get_filename(url)
        filepath = os.path.join(folder_name, filename)
        return drop_illegal_characters(filepath)

    def get_filename(self, url):
        return unquote(url.rsplit('/', maxsplit=1)[1])

    def get_folder_name(self):
        tags = ' '.join(self.tags)
        return f'{self.title} [{tags}]'


@dataclass
class PixivIllustItem:
    """Pixiv Illust"""
    id: int = field(default=None)
    title: str = field(default=None)
    tags: list = field(default_factory=list)
    referer: str = field(default=None)
    original_image_urls: list = field(default=None)

    def get_filename(self, pk, ext):
        """pk is file_id, ext is file extension"""
        tags = ' '.join(map(
            lambda s: drop_illegal_characters(s).replace(' ', '_'),
            (tag.get('translated_name') or tag.get('name', '') for tag in self.tags)
        ))
        title = drop_illegal_characters(self.title)
        return f'{pk} {title} [{tags}].{ext}'


@dataclass
class YanderePostItem:
    """Yandere Post"""
    id: int = field(default=None)
    file_url: str = field(default=None)

    def get_filename(self):
        filename = self.file_url.rsplit('/', maxsplit=1)[1]
        filename = unquote(filename)
        filename = drop_illegal_characters(filename)
        return filename


@dataclass
class LemonPicPostItem:
    id: int = field(default=None)
    title: str = field(default=None)
    image_urls: List = field(default_factory=list)
    tags: List = field(default_factory=list)
    referer: str = field(default=None)

    def get_filename(self, url):
        tags = ' '.join(self.tags)
        folder = f'{self.title} [{tags}]'
        name = url.rsplit('/', maxsplit=1)[1]
        filename = os.path.join(folder, name)
        return drop_illegal_characters(filename)


@dataclass
class NHentaiGalleryItem(BaseItem):
    characters: List = field(default=None)
