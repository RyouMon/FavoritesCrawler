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


def original_url_from_nhentai_thumb_url(url):
    """replace 't' with 'i' in domain, remove 't' from filename.
    'https://t2.nhentai.net/galleries/154829234522/4t.png'
             |                                      |
    'https://i2.nhentai.net/galleries/154829234522/4.png'
    """
    return re.sub(r'https://t(.+/\d+)t(\..+)', r'https://i\g<1>\g<2>', url)
