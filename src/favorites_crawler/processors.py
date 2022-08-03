import re
from datetime import datetime

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
        if (t.startswith('[') and t.endswith(']')) or (t.startswith('(') and t.endswith(']')) \
                or (t.startswith('(') and t.endswith(')')):
            titles.remove(t)

    if titles:
        return titles[0]
    else:
        return ''


def clean_nhentai_title(title):
    if not title:
        return ''

    match = re.match(r'^\[.+\] (.+) \[.+\]$', title)
    if match:
        title = match.group(1)

    match = re.match(r'^(.+) \| .+$', title)
    if match:
        title = match.group(1)

    while title.endswith('.'):
        title = title[:-1]

    return title


def get_year_from_iso_format(iso_format):
    return datetime.fromisoformat(iso_format).year


def get_month_from_iso_format(iso_format):
    return datetime.fromisoformat(iso_format).month


def get_volume_from_title(title):
    match = re.match(r'^.+?(\d+)$', title)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def get_series_from_title(title):
    match = re.match(r'^(.+?)(?:vol.)?\d+$', title)
    if not match:
        return None
    return match.group(1).strip()


def clean_parodies(parodies):
    if not parodies:
        return None

    match = re.match(r'^ *\[.+\]$', parodies)
    if match:
        return None

    match = re.match(r'^ *(.+) \| .+$', parodies)
    if match:
        parodies = match.group(1)

    match = re.match(r'^ *\((.+)\)(?: \[.+\])?$', parodies)
    if match:
        parodies = match.group(1)

    return parodies.strip()
