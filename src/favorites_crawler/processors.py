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


def wrap_credits(artists):
    return [{'person': person, 'role': 'Artist'} for person in artists]


def select_best_nhentai_title(titles):
    if not titles:
        return ''

    titles = [t.strip() for t in titles if t and isinstance(t, str)]

    if not titles:
        return ''

    if len(titles) == 1:
        return titles[0]

    for t in titles.copy():
        if (t.startswith('[') and t.endswith(']')) or (t.startswith('(') and t.endswith(']')):
            titles.remove(t)
        elif t.startswith('(') and t.endswith(')'):
            return t

    if titles:
        return titles[0]
    else:
        return ''


def clean_nhentai_title(title):
    if not title:
        return ''

    match = re.match(r'^.*\((.+)\)$|^\[.+\] (.+) \[.+\]$', title)
    if match:
        title = match.group(1) or match.group(2)

    while title.endswith('.'):
        title = title[:-1]

    return title
