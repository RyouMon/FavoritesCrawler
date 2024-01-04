from zipfile import ZipFile
from pathlib import Path

import pytest

from favorites_crawler.utils.files import create_comic_archive, list_yandere_post


@pytest.fixture
def comic_path(tmp_path):
    comic = tmp_path / 'comic'
    comic.mkdir()

    page1 = comic / '1.jpg'
    page1.write_bytes(b'')

    page2 = comic / '2.jpg'
    page2.write_bytes(b'')

    return comic


class TestCreateComicArchive:

    def test_should_create_an_cbz_archive(self, comic_path):
        tmp_path = comic_path.resolve().parent

        create_comic_archive(comic_path)

        files = [p.name for p in tmp_path.iterdir()]
        assert files == ['comic.cbz']

    def test_cbz_archive_should_contains_page(self, comic_path):
        comic_archive = create_comic_archive(comic_path)

        with ZipFile(comic_archive) as zf:
            assert sorted(zf.namelist()) == ['1.jpg', '2.jpg']

    def test_should_write_comment_to_archive(self, comic_path):
        comic_archive = create_comic_archive(comic_path, comment=b"I'm a comic.")

        with ZipFile(comic_archive) as zf:
            assert zf.comment == b"I'm a comic."


class TestListYanderePost:

    def test_list_yandere_id(self, tmp_path: Path):
        pictures = [
            tmp_path / 'yande.re 1 b c m.jpg',
            tmp_path / 'yande.re 2 b c m.png',
            tmp_path / 'yande.re 10 b c m.jpg',
            tmp_path / 'yande.re 20 b c m.jpeg',
        ]
        for p in pictures:
            p.touch()
        (tmp_path / 'sub').mkdir()
        (tmp_path / 'sub' / 'yande.re 2 b c m.jpeg').touch()

        actual = list_yandere_post(tmp_path)
        actual = {k: v.name for k, v in actual.items()}

        assert actual == {
            '1': 'yande.re 1 b c m.jpg',
            '2': 'yande.re 2 b c m.png',
            '10': 'yande.re 10 b c m.jpg',
            '20': 'yande.re 20 b c m.jpeg'
        }

    def test_list_yandere_id_include_subdir(self, tmp_path: Path):
        (tmp_path / 'yande.re 1 b c m.jpg').touch()
        (tmp_path / 'sub').mkdir()
        (tmp_path / 'sub' / 'yande.re 2 b c m.jpeg').touch()
        (tmp_path / 'sub2').mkdir()
        (tmp_path / 'sub2' / 'yande.re 3 b c m.jpeg').touch()

        actual = list_yandere_post(tmp_path, include_subdir=True)
        actual = {k: v.name for k, v in actual.items()}

        assert actual == {
            '1': 'yande.re 1 b c m.jpg',
            '2': 'yande.re 2 b c m.jpeg',
            '3': 'yande.re 3 b c m.jpeg',
        }
