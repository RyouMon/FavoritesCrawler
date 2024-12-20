import typer

import favorites_crawler.commands.login
import favorites_crawler.commands.crawl
import favorites_crawler.commands.restore

__version__ = '1.0.0'

app = typer.Typer(
    help='Crawl your personal favorite images, photo albums, comics from website.',
    no_args_is_help=True,
)
app.add_typer(favorites_crawler.commands.login.app, name='login')
app.add_typer(favorites_crawler.commands.crawl.app, name='crawl')
app.add_typer(favorites_crawler.commands.restore.app, name='restore')


def main():
    app()


if __name__ == '__main__':
    main()
