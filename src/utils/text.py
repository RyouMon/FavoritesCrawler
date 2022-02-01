import re

from constants.regexes import ILLEGAL_FILENAME_CHARACTERS


def drop_illegal_characters(text: str, pattern=ILLEGAL_FILENAME_CHARACTERS) -> str:
    return re.sub(pattern, '', text)
