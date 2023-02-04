import json
import datetime
import os.path
from dataclasses import dataclass, field, fields
from urllib.parse import unquote

from favorites_crawler import __version__
from favorites_crawler.utils.text import drop_illegal_characters


@dataclass
class BaseItem:
    id: int = field(default=None)
    title: str = field(default=None)
    file_urls: list = field(default=None)
    tags: list = field(default=None)
    referer: str = field(default=None)

    def get_filepath(self, url, spider):
        folder_name = self.get_folder_name(spider)
        filename = self.get_filename(url, spider)
        return os.path.join(folder_name, filename)

    def get_filename(self, url, spider):
        return drop_illegal_characters(unquote(url.rsplit('/', maxsplit=1)[1]))

    def get_folder_name(self, spider):
        name = self.title
        if not name:
            name = str(datetime.date.today())
        return drop_illegal_characters(name)


@dataclass
class ComicBookInfoItem:

    title: str = field(default=None, metadata={'is_comic_info': True})
    series: str = field(default=None, metadata={'is_comic_info': True})
    publisher: str = field(default=None, metadata={'is_comic_info': True})
    publicationMonth: int = field(default=None, metadata={'is_comic_info': True})
    publicationYear: int = field(default=None, metadata={'is_comic_info': True})
    issue: int = field(default=None, metadata={'is_comic_info': True})
    numberOfIssues: int = field(default=None, metadata={'is_comic_info': True})
    volume: int = field(default=None, metadata={'is_comic_info': True})
    numberOfVolumes: int = field(default=None, metadata={'is_comic_info': True})
    rating: int = field(default=None, metadata={'is_comic_info': True})
    genre: str = field(default=None, metadata={'is_comic_info': True})
    language: str = field(default=None, metadata={'is_comic_info': True})
    country: str = field(default=None, metadata={'is_comic_info': True})
    credits: list = field(default=None, metadata={'is_comic_info': True})
    tags: list = field(default=None, metadata={'is_comic_info': True})
    comments: str = field(default=None, metadata={'is_comic_info': True})

    def get_comic_info(self):
        comic_book_info = {}
        for f in fields(self):
            if not f.metadata.get('is_comic_info', False):
                continue
            val = getattr(self, f.name)
            if not val:
                continue
            comic_book_info[f.name] = val

        return json.dumps({
            'appID': f'FavoritesCrawler/{__version__}',
            'lastModified': str(datetime.datetime.now()),
            'ComicBookInfo/1.0': comic_book_info,
        }, ensure_ascii=False)


@dataclass
class PixivIllustItem(BaseItem):

    user_id: str = field(default=None)

    def get_folder_name(self, spider):
        if not spider.crawler.settings.getbool('FAVORS_PIXIV_ENABLE_ORGANIZE_BY_USER'):
            return ''
        return self.user_id or 'unknown'


@dataclass
class YanderePostItem(BaseItem):

    def get_folder_name(self, _):
        return ''


@dataclass
class LemonPicPostItem(BaseItem, ComicBookInfoItem):
    title: str = field(default=None, metadata={'is_comic_info': True})
    tags: list = field(default=None, metadata={'is_comic_info': True})


@dataclass
class NHentaiGalleryItem(BaseItem, ComicBookInfoItem):
    title: str = field(default=None, metadata={'is_comic_info': True})
    tags: list = field(default=None, metadata={'is_comic_info': True})
    parodies: str = field(default=None)
    characters: list = field(default=None)
    sort_title: str = field(default=None)

    def get_folder_name(self, _):
        return drop_illegal_characters(self.sort_title)
