import os
from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

from favorites_crawler.utils import auth
from favorites_crawler.utils.config import load_config, overwrite_settings

__version__ = '0.1.5'

os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'favorites_crawler.settings')
scrapy_settings = get_project_settings()
spider_loader = SpiderLoader(scrapy_settings)
overwrite_settings(spider_loader, scrapy_settings, load_config())

login_processors = {
    'pixiv': auth.login_pixiv,
    'yandere': auth.auth_yandere,
}


def crawl(name):
    process = CrawlerProcess(scrapy_settings)
    process.crawl(name)
    process.start()


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    parser.set_defaults(func=lambda _: parser.print_usage())

    login_parser = subparsers.add_parser('login', help='login help')
    login_parser.add_argument('name', choices=login_processors.keys())
    login_parser.set_defaults(func=lambda ns: login_processors[ns.name]())

    crawl_parser = subparsers.add_parser('crawl', help='crawl help')
    crawl_parser.add_argument('name', choices=spider_loader.list())
    crawl_parser.set_defaults(func=lambda ns: crawl(ns.name))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
