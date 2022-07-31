from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile


def create_comic_archive(path: Path, comment=b''):
    archive_name = path.resolve().parent / f'{path.name}.cbz'
    with ZipFile(archive_name, 'x') as zf:
        zf.comment = comment
        for f in path.iterdir():
            if not f.is_file():
                continue
            zf.write(f, f.name)

    rmtree(path, ignore_errors=True)

    return archive_name
