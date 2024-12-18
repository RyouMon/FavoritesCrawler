from __future__ import annotations

import json
from pathlib import Path
from shutil import rmtree
from typing import Any
from zipfile import ZipFile

from loguru import logger

from favorites_crawler.utils.text import get_yandere_post_id


def create_comic_archive(path: Path, comic_info: dict | None = None) -> Path:
    comment = bytes(
        json.dumps(comic_info, ensure_ascii=False),
        encoding='utf-8'
    ) if comic_info else b''

    archive_name = path.resolve().parent / f'{path.name}.cbz'
    with ZipFile(archive_name, 'x') as zf:
        zf.comment = comment
        for f in path.iterdir():
            if not f.is_file():
                continue
            zf.write(f, f.name)

    rmtree(path, ignore_errors=True)
    return archive_name


def list_yandere_post(path=Path('.'), include_subdir=False, result=None):
    result = {} if result is None else result
    for file_or_dir in path.iterdir():
        if file_or_dir.is_file():
            id_ = get_yandere_post_id(file_or_dir.name)
            if id_:
                result[id_] = file_or_dir
        elif include_subdir:
            list_yandere_post(file_or_dir, include_subdir, result)
    return result


def list_comics(path=Path('.'), result=None):
    result = {} if result is None else result
    for file_or_dir in path.iterdir():
        if file_or_dir.is_file():
            id_ = get_comic_id(file_or_dir)
            if id_:
                result[id_] = file_or_dir
        else:
            list_comics(file_or_dir, result)
    return result


def get_comic_id(file: Path) -> Any:
    try:
        with ZipFile(file, 'r') as zf:
            comment = zf.comment.decode(encoding='utf8')
            comic_info = json.loads(comment)
            return comic_info.get('x-FavoritesCrawler', {}).get('id')
    except Exception as e:
        logger.error('Failed to get comic id from {}, {!r}', file, e)
        return None


def load_json(filename):
    with open(filename, encoding='utf8') as f:
        return json.load(f)
