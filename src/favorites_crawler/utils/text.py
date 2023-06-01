import re
from typing import Optional

from favorites_crawler.constants.regexes import ILLEGAL_FILENAME_CHARACTERS


def drop_illegal_characters(text: str, pattern=ILLEGAL_FILENAME_CHARACTERS) -> str:
    return re.sub(pattern, '', text)


def get_yandere_post_id(text: str) -> Optional[str]:
    match = re.match(r'^yande\.re (\d+) .+\..+$', text)
    return match.group(1) if match else None
