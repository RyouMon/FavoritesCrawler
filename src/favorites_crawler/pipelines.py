# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pathlib import Path

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from twisted.python.failure import Failure
from exiftool import ExifToolHelper

from favorites_crawler.utils.files import create_comic_archive


logger = logging.getLogger(__name__)


class BasePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        item_dict = ItemAdapter(item).asdict()
        referer = item_dict.get('referer')
        return (Request(url, headers={'referer': referer}) for url in item_dict.get(self.files_urls_field, ()))

    def file_path(self, request, response=None, info=None, *, item=None):
        return item.get_filepath(request.url, info.spider)

    def item_completed(self, results, item, info):
        for result in info.downloaded.values():
            if isinstance(result, Failure):
                logger.error('Error when downloading file: %r', result.value)
        return super().item_completed(results, item, info)


class PicturePipeline(BasePipeline):
    """Save image and add iptc/keywords to it."""
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func=download_func, settings=settings)
        self.write_iptc_keywords = settings.getbool('ENABLE_WRITE_IPTC_KEYWORDS', False)
        if self.write_iptc_keywords:
            try:
                self.exif_tool = ExifToolHelper(executable=settings.get('EXIF_TOOL_EXECUTABLE', None))
                self.exif_tool.run()
            except Exception as e:
                logger.error('Failed to load exiftool, consider to install it or setting EXIF_TOOL_EXECUTABLE. '
                             '\nException: %r', e)
                self.exif_tool = None
        else:
            self.exif_tool = None

    def close_spider(self, _):
        if self.exif_tool and self.exif_tool.running:
            self.exif_tool.terminate()

    def item_completed(self, results, item, info):
        item = super().item_completed(results, item, info)
        if not self.exif_tool:
            return item

        for success, result in results:
            if not success:
                continue
            # TODO: add setting control it
            if result.get('status') == 'uptodate':
                continue
            path = item.get_filepath(result['url'], info.spider)
            tags = {}
            if item.tags:
                tags['Keywords'] = item.tags
            if item.created_time:
                tags['CreateDate'] = item.created_time
            if item.title:
                tags['Title'] = item.title
            if not tags:
                continue
            try:
                msg = self.exif_tool.set_tags(
                    Path(self.store.basedir) / path,
                    tags,
                    ['-overwrite_original'],
                ).rstrip()
            except Exception as e:
                logger.error('Failed to write tags: %r to "%s", result: %r', tags, path, e)
            else:
                if msg == '1 image files updated':
                    info.spider.crawler.stats.inc_value('iptc_status_count/updated')
                    logger.debug('Success to write tags: %r to "%s", result: %s', tags, path, msg)
                else:
                    logger.error('Failed to write tags: %r to "%s", result: %s', tags, path, msg)

        return item


class ComicPipeline(BasePipeline):
    """Archive comic as cbz and add ComicBookInfo to it."""
    def __init__(self, store_uri, **kwargs):
        super().__init__(store_uri, **kwargs)
        self.files_path = Path(store_uri).resolve()
        self.comic_comments = {}

    def close_spider(self, spider):
        for title, comment in self.comic_comments.items():
            folder = self.files_path / title
            if not folder.exists():
                continue
            try:
                create_comic_archive(folder, comment=comment)
            except FileNotFoundError:
                pass

    def process_item(self, item, spider):
        if hasattr(item, 'get_comic_info'):
            title = item.get_folder_name(spider)
            if (self.files_path / f'{title}.cbz').exists():
                raise DropItem(f'Comic file of "{title}" already exist, stop download this comic.')
            comment = item.get_comic_info()
            self.comic_comments[title] = bytes(comment, encoding='utf-8')

        return super().process_item(item, spider)
