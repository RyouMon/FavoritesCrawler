from zipfile import ZipFile

import pytest

from favorites_crawler.utils.files import create_comic_archive, list_yandere_id


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


def test_list_yandere_id(tmp_path):
    pictures = [
        tmp_path / 'yande.re 1 b c m.jpg',
        tmp_path / 'yande.re 2 b c m.png',
        tmp_path / 'yande.re 10 b c m.jpg',
        tmp_path / 'yande.re 20 b c m.jpeg',
    ]
    for p in pictures:
        p.touch()

    actual = list_yandere_id(tmp_path)

    assert sorted(actual) == ['1', '10', '2', '20']
