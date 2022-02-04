from itemloaders.processors import TakeFirst, Identity

from favorites_crawler.constants.blacklists import PIXIV_TAG_KEYWORD_BLACKLIST


take_first = TakeFirst()
identity = Identity()


def filter_pixiv_tags(tags):
    def filter_tag(tag):
        for v in tag.values():
            for k in PIXIV_TAG_KEYWORD_BLACKLIST:
                if v and k in v:
                    return False
        return True
    return [tag for tag in filter(filter_tag, tags)]
