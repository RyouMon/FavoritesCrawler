# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field

from favorites_crawler.utils.text import drop_illegal_characters


@dataclass
class PixivIllustItem:
    """Pixiv Illust"""
    id: int = field(default=None)
    title: str = field(default=None)
    tags: list = field(default=None)
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
