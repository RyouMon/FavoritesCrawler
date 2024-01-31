import re
from typing import Optional

from unidecode import unidecode
from pykakasi import kakasi
from langdetect import detect as detect_language

from favorites_crawler.constants.regexes import ILLEGAL_FILENAME_CHARACTERS

kks = kakasi()


def drop_illegal_characters(text: str, pattern=ILLEGAL_FILENAME_CHARACTERS) -> str:
    return re.sub(pattern, '', text)


def get_yandere_post_id(text: str) -> Optional[str]:
    match = re.match(r'^yande\.re (\d+) .+\..+$', text)
    return match.group(1) if match else None


def ascii_tag(text: Optional[str]) -> str:
    if not text:
        return ''
    language = detect_language(text)
    if language == 'ja':
        result = '_'.join(map(lambda r: r.get('hepburn', ''), kks.convert(text)))
    else:
        result = unidecode(text)
    return result.lower().strip().replace(' ', '_')
