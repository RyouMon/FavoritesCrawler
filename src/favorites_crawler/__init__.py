import os
from logging import getLogger
from argparse import ArgumentParser

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

from favorites_crawler.utils import auth
from favorites_crawler.utils.config import load_config, overwrite_settings

__version__ = '0.2.1'

logger = getLogger(__name__)

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'favorites_crawler.settings')
scrapy_settings = get_project_settings()
spider_loader = SpiderLoader(scrapy_settings)
overwrite_settings(spider_loader, scrapy_settings, load_config())

login_processors = {
    'pixiv': auth.login_pixiv,
    'yandere': auth.auth_yandere,
    'twitter': auth.auth_twitter,
}


def crawl(name, **kwargs):
    process = CrawlerProcess(scrapy_settings)
    process.crawl(name, **kwargs)
    for crawler in process.crawlers:
        crawler.signals.connect(spider_closed, signal=signals.spider_closed)
    process.start()


def spider_closed(spider):
    stats = spider.crawler.stats.get_stats()
    if not (stats.get('item_scraped_count', 0) + stats.get('item_dropped_count', 0)):
        logger.warning('Your cookies or token may have expired.')


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='')
    parser.set_defaults(func=lambda _: parser.print_usage())

    login_parser = subparsers.add_parser('login', help='start logining')
    login_parser.add_argument('name', choices=login_processors.keys())
    login_parser.set_defaults(func=lambda ns: login_processors[ns.name]())

    crawl_parser = subparsers.add_parser('crawl', help='crawl help')
    crawl_parser.add_argument('name', choices=spider_loader.list())
    crawl_parser.add_argument('--id', '-i', action='store', nargs='*', dest='id_list')
    crawl_parser.set_defaults(func=lambda ns, **kwargs: crawl(ns.name, **kwargs))

    restore_parser = subparsers.add_parser('restore', help='restore help')
    restore_subparser = restore_parser.add_subparsers()
    restore_yandere_parser = restore_subparser.add_parser('yandere')
    restore_yandere_parser.add_argument('-s', '--score', type=int, choices=(0, 1, 2, 3), required=True,
                                        help='Set 1, 2 or 3 to vote, 0 to cancel vote.')
    restore_yandere_parser.add_argument('-t', '--csrf-token', required=True,
                                        help='CSRF token. To get it: '
                                             '1. Open your browser DevTools. '
                                             '2. Switch to network tab. '
                                             '3. Vote any post on yandere. '
                                             '4. Copy x-csrf-token value from request headers.')
    restore_yandere_parser.add_argument('-c', '--cookie', required=True,
                                        help='Cookie. To get it: '
                                             '1. Open your browser DevTools. '
                                             '2. Switch to network tab. '
                                             '3. Vote any post on yandere. '
                                             '4. Copy cookie value from request headers. ')
    restore_yandere_parser.add_argument('path', help='The location of the post to vote. (Sub-folders are ignored)')
    restore_yandere_parser.set_defaults(
        func=lambda ns: crawl('yandere_vote', score=ns.score, csrf_token=ns.csrf_token, cookie=ns.cookie, path=ns.path))

    args = parser.parse_args()
    try:
        args.func(args, id_list=args.id_list)
    except (TypeError, AttributeError):
        args.func(args)


if __name__ == '__main__':
    main()
