import os

import typer
from rich import print
from rich.panel import Panel
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

from favorites_crawler.constants.domains import LMMPIC_DOMAIN, NHENTAI_DOMAIN, TWITTER_DOMAIN
from favorites_crawler.utils.config import load_config, overwrite_spider_settings
from favorites_crawler.utils.common import get_favors_home
from favorites_crawler.utils.auth import refresh_pixiv_token
from favorites_crawler.utils.cookies import load_cookie

app = typer.Typer(help='Crawl your favorites from websites.', no_args_is_help=True)

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'favorites_crawler.settings')
scrapy_settings = get_project_settings()
spider_loader = SpiderLoader(scrapy_settings)


@app.command('yandere')
def crawl_yandere():
    """Crawl your favorite posts from yandere."""
    crawl('yandere')


@app.command('pixiv')
def crawl_pixiv():
    """Crawl your favorite illustrations from pixiv."""
    favors_home = get_favors_home()
    try:
        access_token = refresh_pixiv_token(favors_home)
    except Exception as e:
        print(e)
        exit(1)
    crawl('pixiv', access_token=access_token)


@app.command('nhentai')
def crawl_nhentai():
    """Crawl your favorite comics from nhentai."""
    favors_home = get_favors_home()
    cookies = load_cookie(NHENTAI_DOMAIN, favors_home)
    crawl('nhentai', cookies=cookies)


@app.command('x')
@app.command('twitter')
def crawl_twitter():
    """Crawl your favorite pictures from twitter."""
    favors_home = get_favors_home()
    cookies = load_cookie(TWITTER_DOMAIN, favors_home)
    crawl('twitter', cookies=cookies)


@app.command('lemon')
def crawl_lemon(id_list: list[str] = typer.Option([], '--id', '-i')):
    """Crawl your favorite photo albums from lemon."""
    favors_home = get_favors_home()
    cookies = load_cookie(LMMPIC_DOMAIN, favors_home)
    crawl('lemon', id_list=id_list, cookies=cookies)


def spider_closed(spider):
    """Will call when spider closed."""
    stats = spider.crawler.stats.get_stats()
    print('Dumping Scrapy stats:', stats)
    if spider.name == 'yandere_vote':
        return
    if stats.get('finish_reason') == 'fastly-finished':
        return
    elif not (stats.get('item_scraped_count', 0) + stats.get('item_dropped_count', 0)):
        print(Panel(
            '[red]Nothing was crawled, your cookies or token may have expired.',
            border_style="red",
            title="Warning",
            title_align="left",
        ))


def crawl(name, **kwargs):
    """
    Crawl spider.
    :param name: spider name
    :param kwargs: kwargs passed to spider's __init__ method
    """
    spider = spider_loader.load(name)
    favors_home = get_favors_home()
    overwrite_spider_settings(spider, favors_home, load_config(favors_home))
    process = CrawlerProcess(scrapy_settings)
    process.crawl(spider, **kwargs)
    for crawler in process.crawlers:
        crawler.signals.connect(spider_closed, signal=signals.spider_closed)
    process.start()
