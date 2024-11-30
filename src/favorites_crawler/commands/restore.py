import typer
from rich import print
from rich.panel import Panel
from typer.rich_utils import STYLE_ERRORS_PANEL_BORDER, ERRORS_PANEL_TITLE, ALIGN_ERRORS_PANEL

from favorites_crawler.commands.crawl import crawl

app = typer.Typer(help='Restore your favorites to websites.', no_args_is_help=True)


@app.command('yandere')
def restore_yandere(
        score: int = typer.Option(
            ..., '-s', '--score', help='Set 1, 2 or 3 to vote, 0 to cancel vote.',
            show_choices=True, min=0, max=3
        ),
        csrf_token: str = typer.Option(
            ..., '-t', '--csrf-token',
            help='CSRF token. To get it: '
                 '1. Open your browser DevTools. '
                 '2. Switch to network tab. '
                 '3. Vote any post on yandere. '
                 '4. Copy x-csrf-token value from request headers.'),
        cookie: str = typer.Option(
            ..., '-c', '--cookie',
            help='Cookie. To get it: '
                 '1. Open your browser DevTools. '
                 '2. Switch to network tab. '
                 '3. Vote any post on yandere. '
                 '4. Copy cookie value from request headers.'
        ),
        path: str = typer.Argument(
            '.', help='The location of the post to vote. (Sub-folders are ignored)'
        )
):
    try:
        cookies = {}
        for pair in cookie.split('; '):
            k, v = pair.split('=')
            cookies[k] = v
    except Exception as e:
        print(Panel(
            f'[red]Failed to parse cookies! {e!r}',
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title=ERRORS_PANEL_TITLE,
            title_align=ALIGN_ERRORS_PANEL,
        ))
    else:
        crawl('yandere_vote', score=score, csrf_token=csrf_token, cookies=cookies, path=path)
