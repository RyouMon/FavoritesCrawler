import re
from typing import Optional

from unidecode import unidecode
from pykakasi import kakasi
from langdetect import detect as detect_language
from langdetect import LangDetectException

from favorites_crawler.constants.regexes import ILLEGAL_FILENAME_CHARACTERS

kks = kakasi()


def drop_illegal_characters(text: str, pattern=ILLEGAL_FILENAME_CHARACTERS) -> str:
    return re.sub(pattern, '', text)


def get_yandere_post_id(text: str) -> Optional[str]:
    match = re.match(r'^yande\.re (\d+) .+\..+$', text)
    return match.group(1) if match else None


def convert_to_ascii(text: Optional[str], replace_space=True) -> str:
    if not text:
        return ''
    try:
        language = detect_language(text)
    except LangDetectException:
        language = 'unknown'
    if language == 'ja':
        result = '_'.join(map(lambda r: r.get('hepburn', ''), kks.convert(text)))
    else:
        result = unidecode(text)
    if replace_space:
        result = result.strip().replace(' ', '_')
    return result.lower().strip()
