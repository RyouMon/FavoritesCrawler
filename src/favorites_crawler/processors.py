import re

from itemloaders.processors import TakeFirst, Identity


take_first = TakeFirst()
identity = Identity()


def get_nhentai_id(url):
    """Get comic ID from comic url"""
    match = re.match(r'https.+g/(\d+)/', url)
    if not match:
        return ''
    return match.group(1)


def replace_space_with_under_scope(text):
    return '_'.join(text.split())
